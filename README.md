# bme590hrm

The following repository contains 2 main module functions, HRMData.py and test_HRM.py

test_HRM is the test code for HRMData.py

HRMData.py takes in 4 arguments, dataStr, interval, threshold and minDist

dataStr is the first argument where the user must input the name of the csv file they want to have analyzed. This input must be filled.

interval is the second user input that may be modified. This determines how many seconds the user wants to analyze the ECG data for.

The next two inputs, threshold and minDist have default values but may be changed to the user's liking. Depending on the frequency and height of the voltage spikes, these may be adjusted to obtain more accurate heart rate measurements.
