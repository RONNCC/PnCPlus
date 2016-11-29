import matplotlib.pyplot as plt
import csv
import re
import sys
import os

# example file_name:  "Total Distinct Patients 8.19.13-8.18.14.csv"
file_name = sys.argv[1]
title_start = file_name.rfind(os.path.sep) + 1
title = file_name[title_start :len(file_name)-4]

date_regex = r'[0-9\-\.]*\.csv$'
date = re.search(date_regex, file_name).group()
#remove file ending
date = date[:len(date)-4]
output_directory = ".." + os.path.sep + "output" + date 
if(not os.path.isdir(os.getcwd() + os.path.sep + output_directory)):
    os.mkdir(output_directory)

PATIENT_COUNT= 1
ACADEMIC_LEVEL= 2

data = []

with open(file_name, "rb") as f:
    reader = csv.reader(f)
    headers = reader.next()

    for row in reader:
        data.append(row)
    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in xrange(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)

fig = plt.figure()
ax = fig.gca()
plt.title(title)
labels=[]
counts = []

for j in xrange(len(data)):
    row = data[j]
    labels.append(row[ACADEMIC_LEVEL] + "(" + row[PATIENT_COUNT] + ")")
    counts.append(row[PATIENT_COUNT])

import numpy as np
y_pos = np.arange(len(labels)) + 0.5

ax.barh(y_pos, counts, align='center', color=tableau20[1])
plt.yticks(y_pos, labels)
plt.xlabel("number of distinct patients")

plt.savefig(output_directory + os.path.sep + title+ " " +
        date + '.eps', bbox_inches='tight')

