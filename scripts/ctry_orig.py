import matplotlib.pyplot as plt
import csv, sys, re
import Tkinter, FileDialog

#example file_name: "International Status, Country of Origin, and Academic Level.csv"
file_name = sys.argv[1]
title = file_name[:len(file_name)-4]
path = "../data/" + file_name

#date_regex = r'[0-9\-\.]*\.csv$'
#date = re.search(date_regex, path).group()
##remove file ending
#date = date[:len(date)-4]
output_directory = "../ctry_orig"
if(not os.path.isdir(os.getcwd() + "/" + output_directory)):
    os.mkdir(output_directory)

ACADEMIC_LVL = 0
INTERNATIONAL_BOOL = 1
COUNTRY = 2

from collections import Counter

all_count = Counter()
international_count = Counter()
domestic_count = Counter()

with open(path, "rb") as f:
    reader = csv.reader(f)
    headers = reader.next()

    for row in reader:
        country = row[COUNTRY].upper()
        if(country != ""):
            acad_lvl = row[ACADEMIC_LVL]
            international = True if row[INTERNATIONAL_BOOL] == "True" else False
    
            all_count[country] += 1

            if(international):
                international_count[country] += 1
            else:
                domestic_count[country] += 1

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
countries=[]
counts = []

import numpy as np
for country in international_count:
    count = international_count[country]
    countries.append(country)
    counts.append(count)

y_pos = np.arange(len(countries)) +0.5


plt.barh(y_pos, counts, align = 'center', color=tableau20[0])
plt.yticks(y_pos, countries)
plt.xlabel("number of students")

plt.savefig(output_directory + "/" + title+ " " +
        '.eps', bbox_inches='tight')

