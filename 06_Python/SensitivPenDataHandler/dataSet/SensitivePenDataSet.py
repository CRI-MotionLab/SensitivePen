import pandas as pd
import numpy as np
import serial
import tools.displayFunctions as df
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator
import tools.getAngleMethods as gam
import os
import math


class SensitivePenDataSet():
    """
    Class that represent a data set of the sensitiv pen.
    It allows the user to have easily acces to basic movuino data : ax,ay,az,gx,gy,gz,mx,my,mz
    It calulates in the constructor the norm of this basic movuino data.


    """
    def __init__(self, filepath):
        """
        Constructor of the sensitivePen
        :param filepath: filepath of the raw data set
        """
        self.name = "SensitivePen"

        self.filepath = filepath
        self.filename = os.path.basename(self.filepath)
        print("Reading : " + filepath)

        self.rawData = pd.read_csv(filepath, sep=",")

        self.time = []

        # basic data from the movuino
        self.acceleration = np.array([self.rawData["ax"], self.rawData["ay"], self.rawData["az"]])
        self.gyroscope = np.array([self.rawData["gx"], self.rawData["gy"], self.rawData["gz"]]) * 180 / np.pi
        self.magnetometer = np.array([self.rawData["mx"], self.rawData["my"], self.rawData["mz"]])

        # norm of
        self.normAcceleration = np.linalg.norm(self.acceleration, axis=0)
        self.normGyroscope = np.linalg.norm(self.gyroscope, axis=0)
        self.normMagnetometer = np.linalg.norm(self.magnetometer, axis=0)

        # pressure
        #self.pressure = self.rawData["pressure"]
        #self.pressure = np.array(self.pressure)

        # time list in seconds
        self.time = list(self.rawData["time"])

        # sample rate
        self.Te = (self.time[-1] - self.time[0]) / (len(self.time))

        # number of row
        self.nb_row = len(self.time)

        # Relevant angle for the pen
        try :
            #
            self.psi = np.array(self.rawData['psi'])
            self.theta = np.array(self.rawData['theta'])
            self.angle_a_m = np.array(self.rawData["angle_acc_mag"])
        except (KeyError):
            pass


    def computePenAngles(self):
        """
        Calculate psi and theta angle given the accekeration and the magnetometer of the pen

        :param self:
        :return:
        """
        # --- Getting initial euler angles
        print("--- Calculating Sensitive Pen's angles ---")
        #We evaluate here the initial angle of the pen         (ax,ay,az)(t=0)          (mx,my,mz)(t=0)
        initRotationMatrix = gam.rotationMatrixCreation(self.acceleration[:,0], self.magnetometer[:,0])
        self.initPsi = math.atan2(initRotationMatrix[0, 1], initRotationMatrix[0, 0])
        inclinaison = 0
        list_theta = []
        list_psi = []
        angle_a_m = []

        for k in range(len(self.time)):
            # --- Getting rotation matrix from filtered data (ax,ay,az)(t=tk) ~ g         (mx,my,mz)(t=tk)
            rotationMatrix = gam.rotationMatrixCreation(self.acceleration[:,k], self.magnetometer[:,k])

            # --- Get inclinaison of the pen (theta)
            inclinaison = gam.getInclinaison(self.acceleration[:,k])
            theta = inclinaison[0] - 90

            # --- getting orientation of the pen (for psi)
            a00 = rotationMatrix[0, 0]  # N.x
            a01 = rotationMatrix[0, 1]  # E.x

            psi = (math.atan2(a01, a00) - self.initPsi) * 180 / math.pi

            # 0->360°
            if psi<0:
                psi += 360
            elif psi > 360:
                psi -= 360

            """
            #  -180 > 180°
            if -180 > psi >= -360:
                psi += 360
            elif 180 < psi <= 360:
                psi -= 360
            """
            angle_a_m.append(np.arcsin(np.linalg.norm(np.cross(self.acceleration[:,k], self.magnetometer[:,k])/(self.normAcceleration[k]*self.normMagnetometer[k])))*180/np.pi)
            list_theta.append(theta)
            list_psi.append(psi)

            self.angle_a_m = np.array(angle_a_m)
            self.theta = np.array(list_theta)
            self.psi = np.array(list_psi)
        return

    #--------- FILE MANAGE Functions -------------------
    def stockData(self, filepath):
        """

        :param self:
        :param folderpath:
        :return:
        """

        dir = os.path.dirname(filepath)
        if not os.path.exists(os.path.dirname(filepath)) :
            os.makedirs(dir)
        self.rawData["normAccel"] = self.normAcceleration
        self.rawData["normMag"] = self.normMagnetometer
        self.rawData["normGyr"] = self.normGyroscope
        self.rawData["psi"] = self.psi
        self.rawData["theta"] = self.theta
        self.rawData["angle_acc_mag"] = self.angle_a_m

        self.rawData.to_csv(filepath, sep=",", index=False, index_label=False)

    @staticmethod
    def movuinoExtraction(serialPort, path):
        isReading = False
        ExtractionCompleted = False
        print("-> Opening serial port {}".format(serialPort))
        arduino = serial.Serial(serialPort, baudrate=115200, timeout=1.)
        # Send read SPIFF instruction to Movuino
        arduino.write(bytes("r", 'ascii'))

        line_byte = ''
        line_str = ''
        datafile = ''
        nbRecord = 1

        while ExtractionCompleted != True:
            line_byte = arduino.readline()
            line_str = line_byte.decode("utf-8")

            if "XXX_end" in line_str and isReading == True :
                isReading = False
                ExtractionCompleted = True
                print("End of data sheet")

                with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                    print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
                    file.write(datafile)

            if "XXX_newRecord" in line_str and isReading == True :

                with open(path + "_" + str(nbRecord) + ".csv", "w") as file:
                    print("Add new file : {}".format(path + "_" + str(nbRecord) + ".csv"))
                    file.write(datafile)

                datafile = ''
                line_str = ''
                nbRecord += 1

            if (isReading):
                if line_str != '':
                    datafile += line_str.strip() + '\n'

            if ("XXX_beginning" in line_str):
                isReading = True
                print("Record begins")


    #--------- DISPLAY Functions -----------------------
    def dispRawData(self):
        """
        Display only basic movuino data
        :return:
        """
        time_list = self.time
        if time_list[-1]%1000 != 0:
            time_list = [t/1000 for t in time_list]
        df.plotVect(time_list, self.acceleration, 'Acceleration (m/s2)', 221)
        df.plotVect(time_list, self.magnetometer, 'Magnetometer', 222)
        df.plotVect(time_list, self.gyroscope, 'Gyroscope (deg/s)', 223)
        """
        pressure = plt.subplot(224)
        pressure.plot(time_list, self.pressure)
        pressure.set_title('Pressure (pressure unit)')
        """
        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        plt.legend(handles=[patchX, patchY, patchZ], loc="upper right", bbox_to_anchor=(2.5, 3.6), ncol=1)

        plt.show()

    def dispProcessedData(self):
        """
        Display norm, angles and basic movuino data
        :return:
        """
        parameters = {'axes.labelsize': 5,
                      'axes.titlesize': 10}
        plt.rcParams.update(parameters)
        time_list = list(self.rawData["time"])

        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        #plt.legend(handles=[patchX, patchY, patchZ], loc="upper right",ncol=1)

        if time_list[-1]%1000 != 0:
            time_list = [t/1000 for t in time_list]
        df.plotVect(time_list, self.acceleration, 'Acceleration (m/s2)', 331)

        df.plotVect(time_list, self.magnetometer, 'Magnetometer', 332)
        df.plotVect(time_list, self.gyroscope, 'Gyroscope (deg/s)', 333)


        acc=plt.subplot(331)
        acc.legend(handles=[patchX, patchY, patchZ], loc="upper left",ncol=1)


        normMag = plt.subplot(335)
        normMag.plot(time_list, self.normMagnetometer, color="black", label="norm")
        normMag.grid(b=True, which='major')
        normMag.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        normMag.tick_params(axis='y', which='minor', labelsize=10, color="#999999")
        normMag.minorticks_on()
        normMag.set_yticks([-10,0,50,100])
        normMag.yaxis.set_minor_locator(MultipleLocator(10))
        normMag.set_title("Norm Magnetometer")

        normAcc = plt.subplot(334)
        normAcc.plot(time_list, self.normAcceleration, color="black", label="norm")
        normAcc.legend(loc='upper left')
        normAcc.grid(b=True, which='major')
        normAcc.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        normAcc.tick_params(axis='y', which='minor', labelsize=10, color="#999999")
        normAcc.minorticks_on()
        normAcc.set_yticks([-10,0,50])
        normAcc.yaxis.set_minor_locator(MultipleLocator(10))
        normAcc.set_title("Norm Acceleration")
        """
        pressure = plt.subplot(339)
        pressure.plot(time_list, self.pressure)
        pressure.set_title('Pressure (pressure unit)')
        """
        sensitivePenAngle = plt.subplot(336)
        sensitivePenAngle.plot(time_list, self.psi, markersize=3,   color="red", alpha=0.7, label='psi')
        sensitivePenAngle.plot(time_list, self.theta, markersize=3, color="blue", alpha=0.7, label='theta')
        sensitivePenAngle.grid(b=True, which='major')
        sensitivePenAngle.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        sensitivePenAngle.tick_params(axis='y', which='minor', labelsize=12, color="#999999")
        sensitivePenAngle.minorticks_on()
        sensitivePenAngle.set_yticks([0, 90, 180, 270, 360])
        sensitivePenAngle.set_ylim(-40, 400)
        sensitivePenAngle.yaxis.set_minor_locator(MultipleLocator(45))
        sensitivePenAngle.legend(loc='upper right')
        sensitivePenAngle.set_title("Relevant angle (psi, theta) (deg)")

        """
        patchX = mpatches.Patch(color='red', label='x')
        patchY = mpatches.Patch(color='green', label='y')
        patchZ = mpatches.Patch(color='blue', label='z')
        plt.legend(handles=[patchX, patchY, patchZ], loc="upper right",ncol=1)
        """

        plt.title(os.path.basename(self.filepath))

        angleAM = plt.subplot(337)
        angleAM.plot(time_list, self.angle_a_m, color="black")
        angleAM.grid(b=True, which='major')
        angleAM.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        angleAM.tick_params(axis='y', which='minor', labelsize=12, color="#999999")
        angleAM.minorticks_on()
        angleAM.set_yticks([-90,0, 90])
        angleAM.yaxis.set_minor_locator(MultipleLocator(10))
        angleAM.set_title("Angle between g and B \n mean : {}, std : {}".format(round(np.mean(self.angle_a_m),1), round(np.std(self.angle_a_m),1)))
        plt.subplots_adjust(hspace=0.4)
        plt.show()

    def dispOnlyPenAngles(self):
        """
        Display pen angles
        :return:
        """
        print("Plotting angles from : {}".format(os.path.basename(self.filepath)))
        time_list = list(self.rawData["time"])
        if time_list[-1]%1000 != 0:
            time_list = [t/1000 for t in time_list]

        sensitivePenAngle = plt.subplot(111)
        sensitivePenAngle.plot(time_list, self.psi, "o", markersize=3,   color="red", alpha=0.3, label='psi')
        sensitivePenAngle.plot(time_list, self.theta, "+", markersize=3, alpha=0.3, color="blue", label='theta')
        sensitivePenAngle.grid(b=True, which='major')
        sensitivePenAngle.grid(b=True, which='minor', color='#999999', linestyle='dotted')
        sensitivePenAngle.tick_params(axis='y', which='minor', labelsize=12, color="#999999")
        sensitivePenAngle.minorticks_on()
        sensitivePenAngle.set_yticks([0, 90, 180, 270, 360])
        sensitivePenAngle.set_ylim(-40, 400)
        sensitivePenAngle.yaxis.set_minor_locator(MultipleLocator(45))
        sensitivePenAngle.legend(loc='upper right')
        sensitivePenAngle.set_title("Relevant angle (psi, theta) (deg)")

        plt.title(os.path.basename(self.filepath))
        plt.show()




