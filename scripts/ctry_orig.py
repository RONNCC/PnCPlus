import matplotlib.pyplot as plt
import csv, sys, re, os
import Tkinter, FileDialog
import numpy as np
import heapq
from collections import Counter

def runReport(path, output_path):
    
    title_start = path.rfind('/') + 1
    title = path[title_start :len(path)-4]
    
    output_directory = output_path + os.path.sep + "ctry_orig"
    if(not os.path.isdir(output_directory)):
        os.mkdir(output_directory)
    
    ACADEMIC_LVL = 0
    INTERNATIONAL_BOOL = 1
    COUNTRY = 2
    NUMBER_OF_CTRY_DISPLAYED = 20
    
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
    heap = []
    
    for country in international_count:
        count = international_count[country]
        heap.append((-1 * count, country))
    
    heapq.heapify(heap)
    y_pos = np.arange(NUMBER_OF_CTRY_DISPLAYED) +0.5
    
    counts = []
    countries = []
    for i in xrange(NUMBER_OF_CTRY_DISPLAYED):
        (count, country) = heapq.heappop(heap)
        counts.append(-1 * count)
        countries.append(country)
    
    countries.reverse()
    counts.reverse()
    
    plt.barh(y_pos, counts, align = 'center', color=tableau20[0])
    plt.yticks(y_pos, countries)
    plt.xlabel("number of students")
    
    plt.savefig(output_directory + "/" + title+ " " +
            '.pdf', bbox_inches='tight')
    plt.close()
