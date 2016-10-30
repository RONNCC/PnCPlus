import sys
import csv
from collections import Counter
from math import log
#fileName = sys.argv[1]
fileName = "data/Appointment_util_Campus_Residence.csv"
with open(fileName, 'rb') as f:
  csvReader = csv.reader(f)
  for row in csvReader:
    for element in row:
      print element
