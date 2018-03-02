import pytest

def test_Norm():
    """ tests some test data with no abnormalities - i.e., ones with no NaN values or string values
    """
    from HRMdata import Data
    fileNames = ['test_data1.csv', 'test_data3.csv', 'test_data23.csv']
    BPM = [78.35, 72.417, 60.832]
    beats = [16, 16, 18]
    totalTime = [27.775, 27.775, 39.996]
    for index, elem in enumerate(fileNames):
        tempObj = Data(dataStr=elem, userInterval=10000)
        assert tempObj.mean_hr_bpm >= BPM[index]-5 or tempObj.mean_hr_bpm <= BPM[index]+5
        assert tempObj.num_beats >= beats[index]-2 or tempObj.num_beats <= beats[index]+2
        assert tempObj.interval == totalTime[index]


def test_Inputs():

    """ tests class calls with abnormal inputs, i.e., calling csv file that doesnt exist or inputting string into userInterval
    first test - intervals greater than length of data are truncated to max length of the original data
    second test - if a csv file that doesnt exist is called, throws FileNotFoundError
    third test - if threshold value is not a number, raises TypeError
    fourth test - if min distance is not a number, raises TypeError
    fifth test - if threshold value is less than 0, raises ValueError
    sixth test - if min dist is less than 0, raises ValueError
    seventh test - if userInterval is negative, raises TypeError
    """
    from HRMdata import Data
    testObj1 = Data(dataStr='test_data1.csv', userInterval=100000)
    assert testObj1.interval == 27.775
    
    with pytest.raises(FileNotFoundError):
        Data(dataStr='hello', userInterval=10000).read_csv()

    with pytest.raises(TypeError):
        Data(dataStr=10, userInterval=10000).read_csv()

    with pytest.raises(TypeError):
        Data(dataStr='test_data1.csv', userInterval = 100000, thr='test').checkThres()

    with pytest.raises(TypeError):
        Data(dataStr='test_data.csv', userInterval = 100000, mD='test').checkMD()

    with pytest.raises(ValueError):
        Data(dataStr='test_data1.csv', userInterval = 100000, thr=-11).checkThres()

    with pytest.raises(ValueError):
        Data(dataStr='test_data1.csv', userInterval = 100000, mD = -12).checkMD()

    with pytest.raises(ValueError):
        Data(dataStr='test_data1.csv', userInterval = -2).checkInterval()
    
    with pytest.raises(TypeError):
        Data(dataStr='test_data1.csv', userInterval='hello').checkInterval()

