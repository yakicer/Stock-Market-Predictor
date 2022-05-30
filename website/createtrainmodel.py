import math
import pandas_datareader as web
from sqlalchemy import Integer
from sqlalchemy import String
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from flask import Flask, request, url_for, redirect, render_template
import sqlite3
import sqlalchemy
import yfinance as yf
import keras
import tensorflow as tf
import os



engine = sqlalchemy.create_engine('sqlite:///database.db')

df = yf.download('AAPL', start='2012-01-01')

data = df.filter(['Close'])


dataset = data.values

training_data_len = math.ceil(len(dataset)* .8)


scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

scaled_data

train_data = scaled_data[0:training_data_len, :]

x_train = []
y_train = []

for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])
    if i<=60:
        print(x_train)
        print(y_train)
        print()

x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()
model.add(LSTM(50, return_sequences= True, input_shape= (x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences= False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train, y_train, batch_size=1, epochs=1)

saved_dir = "my_saved_model"
parent_dir ="C:/Users/Yakup/PycharmProjects/pythonProject4/website"
path = os.path.join(parent_dir, saved_dir)


os.mkdir(path)
model.save('saved_dir/modeldir')
