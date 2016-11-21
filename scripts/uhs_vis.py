import matplotlib.pyplot as plt
import csv
import re

#example file_name: "UHS Exam Room Utilization 8.1.14-7.31.15.csv"
file_name = sys.argv[1]
title = file_name[:len(file_name)-4]
path = "../data/" + file_name

date_regex = r'[0-9\-\.]*\.csv$'
date = re.search(date_regex, path).group()
#remove file ending
date = date[:len(date)-4]
import os
output_directory = "../output" + date 
if(not os.path.isdir(os.getcwd() + "/" + output_directory)):
    os.mkdir(output_directory)

ROOM= 0
COUNT= 1

data = []

with open(path, "rb") as f:
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

plt.title(title)
labels=[]
counts = []

import numpy as np

for j in xrange(len(data)):
    row = data[j]
    labels.append(row[ROOM] + "(" + row[COUNT] + ")")
    counts.append(row[COUNT])

y_pos = np.arange(len(labels)) +0.5


plt.barh(y_pos, counts, align = 'center', color=tableau20[0])
plt.yticks(y_pos, labels)
plt.xlabel("number of appointments")

#Make the pie a circle, not an ellipse
plt.savefig(output_directory + "/" + title+ " " +
        date + '.eps', bbox_inches='tight')
