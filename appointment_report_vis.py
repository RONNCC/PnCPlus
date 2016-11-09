#This script proccesses the Appointment Report by Department and Visit Type
#report. It will output a series of grouped bar graphs into the folder "output"
#that is in the same directory as this program.

import matplotlib.pyplot as plt
import csv, os, sys
import numpy as np 


def makePlotFromCSV(file_name='data/Appointment Report by Department & Visit Type 11.1.16-5.13.16.csv'):
    # Read the data into a pandas DataFrame.    
    # These are the relevant indices from the report csv
    DEPARTMENT_COLUMN = 0
    VISIT_TYPE_COLUMN = 1
    APPTS_COLUMN = 2
    FIRST_DATA_COLUMN = 3;
    LAST_DATA_COLUMN = 6;

    #This dictionary is where the csv's information will be stored
    departments= {}

    #This function takes in a row from the csv and inserts that information
    #into the proper place in the departments dictionary
    def add_row(row):
        department= row[DEPARTMENT_COLUMN].strip()
        if(not departments.has_key(department)):
            departments[department] = ([],[],[])
        visit_types, appts, data = departments[department]
        visit_types.append(row[VISIT_TYPE_COLUMN])
        appts.append(row[APPTS_COLUMN])
        #get rid of the percent sign at the end of each number
        data.append([float(x[0:len(x)-1])
            for x in row[FIRST_DATA_COLUMN:LAST_DATA_COLUMN + 1]])


    with open(file_name, "rb") as f:
        csvReader = csv.reader(f)
        #The very first line of the csv is the header
        headers = csvReader.next()
        for row in csvReader:
            #check if data is present because some rows do not contain data
            if(row[APPTS_COLUMN] != ""):
                add_row(row)

    # These are the "Tableau 20" colors as RGB.    
    tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
                 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
                 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
                 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
                 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
      
    # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
    for i in range(len(tableau20)):    
        r, g, b = tableau20[i]    
        tableau20[i] = (r / 255., g / 255., b / 255.)


    #N is the number of data columns
    N = LAST_DATA_COLUMN - FIRST_DATA_COLUMN + 1
    ind = np.arange(N)

    #for every department, make a new bar graph
    for department, rows in departments.iteritems():
        fig, ax = plt.subplots(figsize=(20,10))
        subplots = []
        width = 0.05
        i = 0
        visits, appts, data = rows
        for datum in data:
            subplots.append(ax.bar(ind + i * width,
                datum, width, color = tableau20[i%len(tableau20)]))
            i += 1
        ax.set_ylabel('percentages')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(headers[FIRST_DATA_COLUMN:LAST_DATA_COLUMN+1])
        ax.set_title(department)
        ax.legend([subplot[0] for subplot in subplots],
            [visit for visit in visits])
        if(not os.path.isdir(os.getcwd() + "/output")):
            os.mkdir("output")
        plt.savefig("output/" + department + '.png', bbox_inches='tight')


