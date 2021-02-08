import math
import numpy as np
import pandas_datareader as web
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import datetime
from datetime import date

#Let's add something that sets the end day to the current day
def dataRetrieve(ticker, startdate, enddate):
    endingDate = date.today();
    df = web.DataReader(ticker, data_source='yahoo', start=startdate, end=endingDate.strftime("%m-%d-%y"));
    dfPred = web.DataReader(ticker, data_source='yahoo', start=startdate, end=enddate);
        
    dateDifference = (enddate - endingDate).days;
    numDataPoints = 60;
    
    #Getting a numpy array from the closing prices
    data = df.filter(['Close']);
    dataPred = df.filter(['Close']);
    dataset = data.values;
    
    #Getting length of training dataset = 80% of the original data
    training_data_len = math.ceil(len(dataset) * .8)
    
    scaler = MinMaxScaler(feature_range=(0,1));
    scaled_data = scaler.fit_transform(dataset);
    
    train_data = scaled_data[0:training_data_len, :];
    
    x_train = [];
    y_train = [];
    
    for i in range(numDataPoints, len(train_data)):
        x_train.append(train_data[i-numDataPoints:i, 0]);
        y_train.append(train_data[i, 0]);

    x_train, y_train = np.array(x_train), np.array(y_train);
    
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1));
    
    #build LSTM model
    model = Sequential();
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)));
    model.add(LSTM(50, return_sequences=False));
    model.add(Dense(25));
    model.add(Dense(1));
    
    #Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error');
    
    model.fit(x_train, y_train, batch_size=1, epochs=1);
    
    test_data = scaled_data[training_data_len - numDataPoints:, :];

    x_test = [];
    x_predict = [];
    y_test = dataset[training_data_len:, :];
    
    for i in range(numDataPoints, len(test_data)):
        x_test.append(test_data[i-numDataPoints:i, 0]);
        if i==numDataPoints:
            x_predict.append(test_data[i-numDataPoints:i, 0]);
        
    x_test = np.array(x_test);
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1));
    
    x_predict = np.array(x_predict);
    x_predict_3d = np.reshape(x_predict, (x_predict.shape[0], x_test.shape[1], 1));
    
    prediction = [];
    predictions = [];
    for i in range(60, len(test_data)+dateDifference):
        prediction = model(x_predict_3d);
        predictions.append(prediction);
        x_predict = x_predict[:, 1:];
        x_predict = np.append(x_predict, prediction);
        x_predict = np.reshape(x_predict, (1, x_predict.shape[0]));
        x_predict_3d = np.reshape(x_predict, (x_predict.shape[0], x_predict.shape[1], 1));
    
    print(len(test_data));
    print(len(test_data)+dateDifference);
    #predictions = model.predict(x_test);
    predictions = np.array(predictions);
    #print(predictions.shape());
    predictions = np.reshape(predictions, (predictions.shape[0], predictions.shape[1]));
    predictions = scaler.inverse_transform(predictions);
    
    #dateList = [];
    #for i in range(0, dateDifference+predictions.shape[0]):
    #    dateList.append((endingDate + datetime.timedelta(days=i-predictions.shape[0]+1) - datetime(1970, 1, 1, 0, 0, 0)).days);
    #print(dateList);
    
    #rmse = np.sqrt(np.mean(predictions - y_test) ** 2);
    
    train = data[:training_data_len];
    valid = data[training_data_len:];
    validPred = dataPred[training_data_len:];
    validPred['Predictions'] = predictions;
    
    return train['Close'], valid['Close'], validPred['Predictions'];
    
    #plt.style.use('fivethirtyeight');
    #plt.figure(figsize=(16,8));
    #plt.title('Ticker:'+ticker);
    #plt.xlabel('Date', fontsize=18);
    #plt.ylabel('Closing Price($)', fontsize=18);
    #plt.plot(train['Close']);
    #plt.plot(valid[['Close', 'Predictions']]);
    #plt.legend(['Train', 'Actual', 'Prediction'], loc='lower right');
    #plt.show();