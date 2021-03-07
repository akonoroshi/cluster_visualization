import os
import re
import csv
import json
import glob
import pandas as pd

'''
1. Task 1: 15
2. Task 2: 15
3. Task 3: 20
4. Task 4: 20 + 5 (for code style which can be ignored)
'''
task = 'task4'
max_score = 20
dataDir = './F19_Project_3_2/' + task + '/'
cmuCS = '@andrew.cmu.edu_social-network_p32-' + task + '_'
timestampDict = {}
mapper = pd.read_csv('./F19_Project_3_2/mapper_anon.csv')

with open('./F19_Project_3_2/gradingdocuments_anon.json') as f:
    grades_str = f.read()
    grades_list = grades_str.split('{"_id":')
    del grades_list[0]

grades = {}
with open(dataDir + 'input.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Project_id", "Source_file_id", "Compile_time", "File_path", "Source_code", "Diff", "Is_last_diff", 
        "Session_id", "Compile_id", "Original_file_id", "Is_correct", "Does_compile", "Source_code_json", "Is_annotated", "Cluster_id"])

    for sub in grades_list:
        sub = '{"_id":' + sub
        grade = json.loads(sub)

        if grade['taskId'] != 'p32-' + task:
            continue
    
        filename = mapper[mapper['gradingDocumentId'] == grade['_id']['$oid']]['submission_filename']
        filename = re.sub('.tar.gz', '', filename.reset_index(drop=True)[0])
        temp = re.split(cmuCS, filename)
        studentID = int(temp[0])
        timestamp = int(temp[1])
        
        if filename not in os.listdir(dataDir):
            print('Submission made by student', studentID, 'at', timestamp, "isn't in submission data")
        else:
            try:
                score = grade['score']
            except KeyError as identifier:
                print('There is no score for submission by', studentID, 'at', timestamp)
                #continue
                score = {task: '0'}
            finally:
                writer.writerow([timestamp, studentID, "", "", "", "", "", "", "", "", int(score[task]) == max_score, "", "", False, ""])
