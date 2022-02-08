import dataSet.SensitivePenDataSet as sp
import tools.FilterMethods as fm
import tools.features_extraction_scripts.runFeature as ft
import os
import numpy as np


############   SETTINGS   #############
device = "sensitiPen"
folderPath = "..\\..\\08_DataPen\\Data_Children\\01_raw_data\\"

fileName = "record"  # generic name numbers will be added for duplicates
serialPort = 'COM4'

filter = 1

sep = ","
decimal = "."

###################################

# --------- Data Extraction from Movuino ----------
"""
Extract data from the serial port and stock it into a csv file
"""
print("Data extraction..")
sp.SensitivePenDataSet.movuinoExtraction(serialPort, folderPath + fileName)
# -------- Data processing ----------------------

for filename in os.listdir(folderPath):
    if os.path.basename(filename).endswith("csv"):
        sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)

        """
        #Filtering
        sensitivPenDataSet.acceleration_lp = fm.MeanFilter(sensitivPenDataSet.acceleration, filter)
        sensitivPenDataSet.gyroscope_lp = fm.MeanFilter(sensitivPenDataSet.gyroscope, filter)
        sensitivPenDataSet.magnetometer_lp = fm.MeanFilter(sensitivPenDataSet.magnetometer, filter)
        """
        #ComputeAngles
        sensitivPenDataSet.computePenAngles()

        #FeaturesDifference between runcode et runfeatures extract
        #ft.getDataSetFeatures(pathfeatures)

        #stock in processed.csv
        treated_filepath = os.path.dirname(sensitivPenDataSet.filepath) + "\\..\\02_treated_data\\" + sensitivPenDataSet.filename[:-4] + "_treated_" + sensitivPenDataSet.name + ".csv"
        sensitivPenDataSet.stockData(treated_filepath)
        sensitivPenDataSet.dispProcessedData()







