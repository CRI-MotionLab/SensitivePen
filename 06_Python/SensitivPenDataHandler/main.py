import dataSet.SensitivePenDataSet as sp
import tools.filterMethods as fm
import tools.features_extraction_scripts.runFeature as ft
import os
import numpy as np

"""
Extract raw data from a Sensitiv Pen. 
It calculates right after the extraction the norm of basic movuino data (acceleration, gyroscope and magnetomter) and
sensitiv pen angles (psi and theta).
This new calculated  data are stored in the same file.

You should specify the folder path and the serial port of the movuino/sensitiv pen
"""

############   SETTINGS   #############

folderPath = "..\\..\\08_DataPen\\Data_Postures\\Manip_061221\\01_raw_data\\"

fileName = "record"  # generic name numbers will be added for duplicates
serialPort = 'COM4'

#######################################

# --------- Data Extraction from Movuino ----------
"""
Extract data from the serial port and stock it into a csv file
"""
print("Data extraction..")
#sp.SensitivePenDataSet.movuinoExtraction(serialPort, folderPath + fileName)
# -------- Data processing ----------------------
for filename in os.listdir(folderPath):
    if os.path.basename(filename).endswith("csv"):
        sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)

        #ComputeAngles
        sensitivPenDataSet.computePenAngles()

        #Stock new calculated data in the csv : norm, and angles
        sensitivPenDataSet.stockData(folderPath + filename)








