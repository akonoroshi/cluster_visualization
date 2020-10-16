from sklearn.manifold import TSNE
from sklearn.manifold import MDS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import SpectralClustering
from sklearn import metrics
import os, sys, subprocess

# Global variables (what you really need here is java_file, data_path, and source_path)
task = 1
# The name of the source file
java_file = ['BankUserConcurrentGet.java', 'BankUserConcurrentPut.java', 'BankUserMultiThreaded.java', 'BankUserStrongConsistency.java'][task-1]
# See get_source_code function of ClusterPlotter class for data_path, source_path, and cmu_cs
# The path to the folder containing different students' source files
data_path = './S20_3.3_OPE_Grading_Anon/3.3_OPE_Submissions-anonymized/'
# The path to the source file folder for each student
source_path = '/src/main/java/Project_OMP/BankUserSystem/'
# You may not need this. This is useful when the names of folders for different students share cmu_cs string.
cmu_cs = '@andrew.cmu.edu_data-consistency-ope_consistency-ope-task_'
# Choose tsne or mds for dimension reduction (lower-case)
embedding = 'mds' 

'''
java_file = ['ProfileServlet.java', 'FollowerServlet.java', 'HomepageServlet.java', 'TimelineServlet.java'][task-1]
data_path = './F19_Project_3_2/task' + str(task) + '/'
cmu_cs = '@andrew.cmu.edu_social-network_p32-task' + str(task) + '_'
'''

class ClusterPlotter:

    def __init__(self, features, clusters, studentID, timestamp, algo_name):
        self.features = features
        self.clusters = clusters
        self.studentID = studentID
        self.timestamp = timestamp
        self.algo_name = algo_name

        self.k=np.unique(clusters).shape[0]

    def plot_all(self):
        x = self.features[:,0]
        y = self.features[:,1]

        fig = plt.figure()
        #fig.suptitle('All clusters together with ' + str(self.clusters.shape[0]) + ' points total')
        fig.suptitle('Task ' + str(task) + ' Solutions: ' + self.algo_name)
        ax = fig.add_subplot(1,1,1)

        #color_points = np.zeros((x.shape[0], 4))
        #for i in range (x.shape[0]):
        #    color_points[i,:] = self.colors[self.clusters[i]]

        ax.scatter(x, y, c=self.clusters, picker=True)
        #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        fig.canvas.mpl_connect('pick_event', lambda e: self.onpick(e, 0))

    def get_source_code(self, i, offset):
        file_path = data_path + str(self.studentID[i]) + cmu_cs + str(self.timestamp[i]) + source_path + java_file
        print('You opened a submission by', str(self.studentID[i]), 'at', str(self.timestamp[i]))
        if sys.platform == "win32":
            os.startfile(file_path)
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_path])
        #with open(file_path.strip(), 'r') as submission_file:
        #    return submission_file.read()

    def onpick(self, event, offset):
        ind = event.ind
        print('-------------------')
        for i in ind:
            self.get_source_code(i, offset)

    def show(self):
        plt.savefig(data_path + '/clusters/task' + str(task) + '/' + self.algo_name + '.png')
        plt.show()

# Embed to 2D
inputCSV = pd.read_csv(data_path + 'input_task{}.csv'.format(task))
data = pd.read_csv(data_path + 'cluster_info_task{}.csv'.format(task))
data['ClusterID'] = data['ClusterID'].fillna(-1)
clusterID = data['ClusterID']
distanceMatrix = data.drop(columns=['StudentID', 'Timestamp', 'ClusterID'])
if embedding == 'tsne':
    reduced = TSNE(n_components=2, metric='precomputed', learning_rate=700, perplexity=40).fit_transform(distanceMatrix)
elif embedding == 'mds':
    reduced = MDS(n_components=2, dissimilarity='precomputed', metric=True).fit_transform(distanceMatrix)
else:
    raise ValueError("Embedding must be either mds or tsne (lower-case)")

# Cluster solutions
cluster_methods = ['optics_xi', 'optics_dbscan', 'dbscan', 'agglomerative_clustering', 'affinity_propagation', 'spectral_clustering']
clusterID_xi = OPTICS(metric='precomputed', max_eps=0.16, xi=0.05, algorithm='brute', min_samples=3).fit_predict(distanceMatrix)
clusterID_op = OPTICS(metric='precomputed', max_eps=0.16, cluster_method='dbscan', min_samples=7).fit_predict(distanceMatrix)
clusterID_db = DBSCAN(metric='precomputed', eps=0.1).fit_predict(distanceMatrix)
clusterID_ag = AgglomerativeClustering(affinity='precomputed', linkage='average', n_clusters=2).fit_predict(distanceMatrix)
clusterID_af = AffinityPropagation(affinity='precomputed', damping=0.7).fit_predict(1 - distanceMatrix)
clusterID_sp = SpectralClustering(affinity='precomputed', n_clusters=2).fit_predict(1 - distanceMatrix)
clusterIDs = [clusterID_xi, clusterID_op, clusterID_db, clusterID_ag, clusterID_af, clusterID_sp]

# Evaluation
for clusterID in clusterIDs:
    try:
        print(metrics.silhouette_score(distanceMatrix, clusterID, metric='precomputed'))
    except ValueError as identifier:
        print("Number of labels is 1. Valid values are 2 to n_samples - 1 (inclusive)")

# Visualize (you may want to change the suffix of the save images)
for i in range(len(cluster_methods)):
    c = ClusterPlotter(reduced, clusterIDs[i], data['StudentID'], data['Timestamp'], '{}_mds'.format(cluster_methods[i]))
    c.plot_all()
    c.show()

# Update clusters in csv
'''
data['ClusterID'] = clusterID_sp
merged = data[['StudentID', 'Timestamp', 'ClusterID']].rename(columns={"StudentID": "Source_file_id", "Timestamp": "Project_id", "ClusterID": "Cluster_Id"})
inputCSV = inputCSV.drop(columns=['Cluster_id'])
inputCSV = inputCSV.merge(merged, how='left', on=["Source_file_id", "Project_id"])

inputCSV.to_csv(data_path + 'input.csv')
'''