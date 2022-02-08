import dataSet.SensitivePenDataSet as sp

folderPath = "..\\..\\08_DataPen\\Data_Children\\01_raw_data\\"
filename = "C1_loops.csv"


sensitivPenDataSet = sp.SensitivePenDataSet(folderPath + filename)
sensitivPenDataSet.stockData(folderPath+sensitivPenDataSet.filename[:-4] + "_treated_" + sensitivPenDataSet.name + ".csv")
import matplotlib.pyplot as plt

sensitivPenDataSet.dispRawData()