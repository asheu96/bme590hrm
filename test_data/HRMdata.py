try:
    import pandas as pd
except ImportError:
    print('Could not import pandas')
try:
    import numpy as np
except ImportError:
    print('Could not import numpy')

try:
    import logging
except ImportError:
    print('Could not import logging')

class Data:
    """ Defines the HRMData class
     Takes in 4 user inputs, dataStr, interval, threshold and minDist
     threshold and minDist are defaulted to 0.18 and 200 respectively if not specified
    :param: dataStr (String) - user input string of datafile to process
    :param: userInterval (int) - user input interval of time in seconds to calculate ECG data information
    :param: thr (double) - user input threshold for peak detection - default to 0.18
    :param: mD (int) - user input mininum distance between peaks - default to 200

    :attribute: csvFile (String) - name of desired CSV file, set to dataStr
    :attribute: csvDf (Pandas Dataframe) - dataframe containing csv file information
    :attribute: times (numpy array) - contains times of ECG data from Dataframe
    :attribute: volt (numpy array) - contains voltage information of ECG data from Dataframe
    :attribute: mean_hr_bpm (double) - avg heart rate over specified interval
    :attribute: voltage_extremes (tuple) - contains min and max lead voltages of data
    :attribute: duration (double) - time duration of ECG strip
    :attribute: num_beats (int) - number of detected beats in ECG strip
    :attribute: beats (numpy array) - time when a beat occured

    """
    def __init__(self, dataStr, userInterval, thr=0.18, mD=200):
        logging.basicConfig(filename='hrmLog.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S')
        with open('hrmLog.txt', 'w'):
            pass

        self.userInterval = userInterval
        self.threshold = thr
        self.minDist = mD

        self.checkInterval()
        self.checkMD()
        self.checkThres()

        self.csvName = dataStr
        self.csvDf = None
        self.times = None
        self.volt = None
        self.read_csv()
        logging.info('csv file has been read')
        self.extract_data()
        logging.info('voltage and time values have been extracted')
        self.duration = None
        self.interval = None
        self.modInterval()
        self.voltage_extremes = None
        self.mean_hr_bpm = None
        self.num_beats = None
        self.beats = None
        logging.info('All attributes have been computed')

    def checkThres(self):
        try:
            self.threshold + 25
        except TypeError:
            print('Threshold must be a number')
            raise TypeError
            return None

        if self.threshold <= 0:
            print('Threshold must be greater than 0')
            logging.debug('Threshold input must be greater than 0')
            raise ValueError('Threshold input must be greater than 0')
        return

    def checkInterval(self):
        if self.userInterval < 0:
            logging.warning('Cannot input negative interval of time')
            raise ValueError('Cannot input negative interval of time')
        try:
            self.userInterval + 25
        except TypeError:
            print('Input must be a number')
            logging.warning('Input entered was not a number')
            raise TypeError
            return None
        return

    def checkMD(self):
        try:
            self.minDist + 25
        except TypeError:
            print('Minimum distance must be a number')
            raise TypeError
            return None

        if self.minDist <= 0:
            print('Minimum distance between peaks must be greater than 0')
            logging.debug('Min distance between peaks must be greater than 0')
            raise ValueError
            return None
        return

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, interval):
        if self.userInterval > self.duration:
            self.__interval = self.duration
        else:
            self.__interval = self.userInterval

    def read_csv(self):
        """ Method used to extract csv file based on given string
        :param: self - contains csvName attribute that contains the name of the file to be read
        :raises: TypeError - if input was not a String file
        :raises: FileNotFoundError - if input file name could no be found
        """
        try:
            self.csvName + 'hello'
        except TypeError:
            print('Input file name must be a String type')
            logging.warning('Input file entered was not a String type')
            raise TypeError('Input file entered was not a String type')
            return None

        try:
            pd.read_csv(self.csvName)
        except FileNotFoundError:
            print('No file with given filename found')
            logging.debug('No file with given filename found')
            raise FileNotFoundError('No file with given filename found')
            return None

        headers = ['Time', 'Voltage']
        df = pd.read_csv(self.csvName, names=headers)
        self.csvDf = df

    def extract_data(self):
        """ Method to extract the time and voltage data points from the csv file dataframe. Converts string values to
        nan values, then interpolates data points. List is then normalized by subtracting the mean
        :param: self - contains the csvDf attribute used to extract the volt and times data
        """
        tempVolt = pd.to_numeric(self.csvDf.Voltage, errors='coerce')
        tempTime = pd.to_numeric(self.csvDf.Time, errors='coerce')

        # if there are any string values, changes them to nan

        self.volt = pd.DataFrame(tempVolt).interpolate().values.ravel().tolist()
        self.times = pd.DataFrame(tempTime).interpolate().values.ravel().tolist()
        self.volt = self.volt - np.mean(self.volt)

    def correlate(self):
        """ Method that correlates two 1D arrays and generates a correlation matrix, starting from time lag 0
        :param: self - contains the voltage vectors used to correlate
        :return: corr - numpy array of the correlation constants, starting from time lag 0
        :raises: ImportError - if math module from Python cannot be imported
        """
        try:
            import math
        except ImportError:
            print('Could not import math package')
            logging.error('Could not import Python math package')

        tempCorr = np.correlate(self.volt, self.volt, mode='same')
        N = len(tempCorr)
        tempCorr = tempCorr[math.floor(N / 2):]
        lengths = range(N, math.floor(N / 2), -1)
        tempCorr /= lengths
        tempCorr /= tempCorr[0]
        return tempCorr

    def modInterval(self):
        """ Method that modulates the voltage interval based on user input
        """
        index = 0
        while self.times[index] < self.interval:
            index += 1

        self.times = self.times[0:index]
        self.volt = self.volt[0:index]

    def writeJSON(self):
        """ Method that writes all calculated attributes into JSON format
        :writes: JSON files with all calculated attributes
        :raises: ImportError - if json module cannot be loaded from Python
        """
        try:
            import json
        except ImportError:
            print('Could not import json module')
            logging.error('Could not import Python module of json')

        out_file = open(self.csvfile + '.json', 'w')
        dataDict = {'Mean HR (BPM)': self.mean_hr_bpm, 'Voltage Extremes': self.voltage_extremes,
                    'Duration': self.duration, 'Number of Beats': self.num_beats, 'Beats': self.beats}
        json.dump(dataDict, out_file)

    def findPeaks(self):
        """ Method that finds the maximum peak indices of the correlated voltage data
        :param: self - contains the voltage vectors used to correlate
        :return: indices - array of the indices at which peaks occur
        :raises: ImportError - if peakutils cannot be imported from Python
        """
        try:
            import peakutils
        except ImportError:
            print('Could not import peakutils')
            logging.error('Could not import peakutils')

        self.minDist = int(self.minDist)
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
        self.__num_beats = len(self.findPeaks())*2

    @property
    def beats(self):
        return self.__beats

    @beats.setter
    def beats(self, beats):
        corrIndex = self.findPeaks()
        stepSize = self.times[1] - self.times[0]
        peakDiff = corrIndex[1]-corrIndex[0]
        beatIndex = []
        for index in range(self.num_beats):
            beatIndex.append(index*peakDiff+corrIndex[0])
        self.__beats = [elem * stepSize for elem in beatIndex]

