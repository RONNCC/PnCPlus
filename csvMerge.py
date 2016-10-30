import sys
import csv
from collections import Counter
from math import log
#fileName = sys.argv[1]
fileName = "data/Appointment Report by Department & Visit Type 11.1.16-5.13.16.csv"
with open(fileName, 'rb') as f:
  csvReader = csv.reader(f)
  for row in csvReader:
    for element in row:
      print element
