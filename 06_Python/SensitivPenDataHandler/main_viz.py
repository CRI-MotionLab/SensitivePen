import dataSet.SensitivePenDataSet as sp
import os

"""
Simple program that allow the user to visualize easily data from the sensitiv pen

The user should specify teh folder path and the name of the file
"""

folderPath = "..\\..\\08_DataPen\\Data_Children\\01_raw_data\\"
filename = "C4_loops.csv"

sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
sensitivPenDataSet.dispProcessedData()

"""
for filename in os.listdir(folderPath):
    if os.path.basename(filename).endswith("csv"):
        sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
        sensitivPenDataSet.dispProcessedData()
"""

