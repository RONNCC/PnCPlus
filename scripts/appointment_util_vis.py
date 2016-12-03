import matplotlib.pyplot as plt
import csv, sys, re, os
import Tkinter, FileDialog

def runReport(input_path, output_path):
    date_regex = r'[0-9\-\.]*\.csv$'
    date = re.search(date_regex, input_path).group()
    #remove file ending
    date = date[:len(date)-4]
    output_directory = output_path + os.path.sep + "Appointment Util" + date 
    if(not os.path.isdir(output_directory)):
        os.mkdir(output_directory)
    
    RESIDENCE = 0
    APPTS = 1
    APPTS_PERC = 2
    LENGTH = 3
    LENGTH_PERC = 4
    CLIENTS = 5
    CLIENTS_PERC = 6
    
    data = []
    
    with open(input_path, "rb") as f:
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
    
    for i in xrange(1, len(headers), 2):
        fig = plt.figure()
        ax = fig.gca()
        header = headers[i]
        plt.title(header)
        percentages = []
        labels=[]
        counts = []
    
        for j in xrange(len(data)):
            row = data[j]
            labels.append(row[RESIDENCE] + "(" + row[i] + ")")
            counts.append(row[i])
            percentages.append(row[i + 1])
        
        ax.pie(counts, labels=labels, colors=tableau20[:len(percentages)],
                autopct='%1.1f%%', startangle=90)
        #Make the pie a circle, not an ellipse
        plt.axis("equal")
        plt.savefig(output_directory + "/" + header+ 
                date + '.eps', bbox_inches='tight')
    
