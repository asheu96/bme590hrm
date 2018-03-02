import pytest

def test_Norm():
    """ tests some test data with no abnormalities - i.e., ones with no NaN values or string values
    """
    from HRMdata import Data
    fileNames = ['test_data1.csv', 'test_data3.csv', 'test_data23.csv']
    BPM = [78.35, 72.417, 60.832]
    beats = [32, 32, 35]
    totalTime = [27.775, 27.775, 39.996]
    for index, elem in enumerate(fileNames):
        tempObj = Data(dataStr=elem, userInterval=10000)
        assert tempObj.mean_hr_bpm >= BPM[index]-5 and tempObj.mean_hr_bpm <= BPM[index]+5
        assert tempObj.num_beats >= beats[index]-2 and tempObj.num_beats <= beats[index]+2
        assert tempObj.interval == totalTime[index]


def test_Inputs():

    """ tests class calls with abnormal inputs, i.e., calling csv file that doesnt exist or inputting string into userInterval
    first test - intervals greater than length of data are truncated to max length of the original data
    second test - if a csv file that doesnt exist is called, throws FileNotFoundError
    third test - if threshold value is not a number, raises TypeError
    fourth test - if min distance is not a number, raises TypeError
    fifth test - if threshold value is less than 0, raises ValueError
    sixth test - if min dist is less than 0, raises ValueError
    seventh test - if userInterval is negative, raises ValueError
    eigth test - if userInterval is not a number, raises TypeError
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
        Data(dataStr='test_data1.csv', userInterval = 'hello').checkInterval()

def test_Abnormal():

    """ tests class calls with abnormal data, i.e., data with missing data or with String 
    """
    from HRMdata import Data
    #fileNames = ['test_data28.csv', 'test_data30.csv', 'test_data31.csv']

    test1 = Data(dataStr='test_data28.csv', userInterval=10000, mD=4)
    assert test1.mean_hr_bpm >= 124.412-10 and test1.mean_hr_bpm <= 124.412+10
    assert test1.num_beats >= 55-4 and test1.num_beats <= 55+4

    test2 = Data(dataStr='test_data30.csv', userInterval=2000, mD=3)
    assert test2.mean_hr_bpm >= 152.329-10 and test2.mean_hr_bpm <= 152.329+10
    assert test2.num_beats >= 100-6 and test2.num_beats <= 100+6

    test3 = Data(dataStr='test_data31.csv', userInterval=2000, thr=0.1, mD=200) 
    assert test3.mean_hr_bpm >= 90-10 and test3.mean_hr_bpm <= 90+10
    assert test3.num_beats >= 17-3 and test3.num_beats <= 17+3       

    test3 = Data(dataStr='test_data32.csv', userInterval=2000, thr=0.1, mD=200) 
    assert test3.mean_hr_bpm >= 90-10 and test3.mean_hr_bpm <= 90+10
    assert test3.num_beats >= 18-3 and test3.num_beats <= 18+3   

def test_json():

    """ tests whether JSON file is written
    """
    from HRMdata import Data
    jsonTest = Data(dataStr='test_data1.csv', userInterval=10000)
    assert jsonTest.writeJSON() == True





