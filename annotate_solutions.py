import os
import re
import csv
import json
import glob
import pandas as pd

task = 4
studentID = '84895'
timestamp = '20191003042705'
annotations = {'Retrieve followers of a user from the Neo4j database here.': (77, 77), 
    'Retrieve the user profile from the SQL database here.' : (78, 78),
    'Retreive the followees of a user from the Neo4j database by writing a new Neo4j query here.': (79, 79), 
    'Retrieve the top comments associated with the followee’s of a user from the MongoDB database here.' : (80, 80),
    'Add the profile and username information to the response here.' : (81, 81)
}

################ Don't Change Below ################

def annotate_dict(annotated):
    start_line = annotated['sourceStart'][0]
    end_line = annotated['sourceEnd'][0]
    for annotation, place in annotations.items():
        if start_line >= place[0] and end_line <= place[1]:
            annotated['annotation'] = annotation
    for child in annotated['children']:
        annotate_dict(child)

if __name__ == "__main__":
    dataDir = './F19_Project_3_2/task' + str(task) + '/'
    cmuCS = '@andrew.cmu.edu_social-network_p32-task' + str(task) + '_'
    java_files = ['ProfileServlet', 'FollowerServlet', 'HomepageServlet', 'TimelineServlet']
    json_path = dataDir + studentID + cmuCS + timestamp + '/' + java_files[task - 1] + '.json'

    with open(json_path, 'r') as f:
        annotated = json.load(f)
        annotated['annotation'] = 'Annotated.'
        annotate_dict(annotated)

    with open(json_path, 'w') as f:
        json.dump(annotated, f, indent=2)

