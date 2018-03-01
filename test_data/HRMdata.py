import pandas as pd
import numpy as np
import json
import math
import logging
import peakutils
#import matplotlib.pyplot as plt

class Data:

    """ Defines the HRMData class
     Takes in 4 user inputs, dataStr, interval, threshold and minDist
     threshold and minDist are defaulted to 0.18 and 200 respectively if not specified
    :Attribute: mean_hr_bpm - avg heart rate over specified interval (double)
    :Attribute: voltage_extremes - contains min and max lead voltages of data (tuple)
    :Attribute: duration - time duration of ECG stripe (double)
    :Attribute: num_beats - number of detected beats in strip (int)
    :Attribute: beats - time when a beat occured (numpy array)
    :Attribute: csvFile - name of desired CSV file (string)
    :Attribute: interval - user-specified number of minutes to read heartbeats (double)
    :Attribute: csvDf - dataframe containing csv file
    """
    def __init__(self, dataStr='test_data1.csv', interval=None, thr=0.18, mD=200):
        logging.basicConfig(filename='hrmLog.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
        with open('hrmLog.txt', 'w'):
            pass
        self.csvName = dataStr
        self.threshold = thr
        self.minDist = mD
        self.csvDf = None
        self.times = None
        self.volt = None
        self.read_csv()
        logging.info('csv file has been read')
        self.extract_data()
        logging.info('voltage and time values have been extracted')
        self.voltage_extremes = None
        self.mean_hr_bpm = None
        self.duration = None
        self.num_beats = None
        self.beats = None

    def read_csv(self):
        """ Method used to extract csv file based on given string
        :param: self - contains csvName attribute that contains the name of the file to be read
        :return: csvDf - a pandas dataframe with the given data
        """
        headers = ['Time', 'Voltage']
        df = pd.read_csv(self.csvName, names=headers)
        self.csvDf = df

    def extract_data(self):
        """ Method to extract the time and voltage data points from the csv file dataframe. Normalizes voltage data
        :param: self - contains the csvDf attribute used to extract the volt and times data
        :return: volt - numpy array of all voltage values of given data
        :return: times - numpy array of all time values of given data
        """
        self.volt = self.csvDf.Voltage.values
        self.volt = self.volt - np.mean(self.volt)
        self.times = self.csvDf.Time.values

    def correlate(self):
        """ Method that correlates two 1D arrays and generates a correlation matrix, starting from time lag 0
        :param: self - contains the voltage vectors used to correlate
        :return: corr - numpy array of the correlation constants, starting from time lag 0
        """
        tempCorr = np.correlate(self.volt, self.volt, mode='same')
        N = len(tempCorr)
        tempCorr = tempCorr[math.floor(N/2):]
        lengths = range(N, math.floor(N/2), -1)
        tempCorr /= lengths
        tempCorr /= tempCorr[0]
        return tempCorr

    def writeJSON(self):
        """ Method that writes all calculated attributes into JSON format
        :writes: JSON files with all calculated attributes
        """
        out_file = open(self.csvfile+'.json', 'w')
        dataDict = {'Mean HR (BPM)': self.mean_hr_bpm, 'Voltage Extremes': self.voltage_extremes,
                    'Duration': self.duration, 'Number of Beats': self.num_beats, 'Beats': self.beats}
        json.dump(dataDict, out_file)

    def findPeaks(self):
        indices = peakutils.indexes(self.correlate(), thres=self.threshold, min_dist=self.minDist)
        return indices

    @property
    def mean_hr_bpm(self):
        return self.__mean_hr_bpm

    @mean_hr_bpm.setter
    def mean_hr_bpm(self, mean_hr_bpm):
        timeVals = [self.times[elem] for elem in self.findPeaks()]
        self.__mean_hr_bpm = len(timeVals) * 60 / (timeVals[len(timeVals) - 1] - timeVals[0])

    @property
    def voltage_extremes(self):
        return self.__voltage_extremes

    @voltage_extremes.setter
    def voltage_extremes(self, voltage_extremes):
        self.__voltage_extremes = (np.min(self.volt), np.max(self.volt))

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = self.times[len(self.times) - 1] - self.times[0]

    @property
    def num_beats(self):
        return self.__num_beats

    @num_beats.setter
    def num_beats(self, num_beats):
        self.__num_beats = len(self.findPeaks())

