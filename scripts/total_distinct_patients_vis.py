import matplotlib.pyplot as plt
import csv
import re

file_name = "Total Distinct Patients 8.19.13-8.18.14.csv"
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

PATIENT_COUNT= 1
ACADEMIC_LEVEL= 2

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

fig = plt.figure()
ax = fig.gca()
plt.title(title)
labels=[]
counts = []

for j in xrange(len(data)):
    row = data[j]
    labels.append(row[ACADEMIC_LEVEL] + "(" + row[PATIENT_COUNT] + ")")
    counts.append(row[PATIENT_COUNT])

ax.pie(counts, labels=labels, colors=tableau20[:len(counts)],
        autopct='%1.1f%%', startangle=90)
#Make the pie a circle, not an ellipse
plt.axis("equal")
plt.savefig(output_directory + "/" + title+ " " +
        date + '.eps', bbox_inches='tight')
