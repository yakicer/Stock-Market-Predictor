import math
import keras
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
import pickle
from flask import Blueprint, render_template, request, redirect, url_for, abort



#engine = sqlalchemy.create_engine('sqlite:///database.db')

#df = pd.read_sql('Crypto', engine)

#data = df.filter(['Close'])

#data

#########################

#dataset = data.values

#training_data_len = math.ceil(len(dataset)* .8)

#training_data_len


#
precision = Blueprint('precision', __name__)


@precision.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        market_data = request.form.get["setvalue"]

        try_quote = web.DataReader(market_data, data_source='yahoo', start='2019-01-01')
        new_df = try_quote.filter(['Close'])
        lst60days = new_df[-60:].values
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(lst60days)
        lst60days_scaled = scaler.transform(lst60days)

        createdmodel = keras.models.load_model('saved_dir/modeldir')

        N_test = []
        N_test.append(lst60days_scaled)
        N_test = np.array(N_test)
        N_test = np.reshape(N_test, (N_test.shape[0], N_test.shape[1], 1))
        pred_price = createdmodel.predict(N_test)
        pred_price = scaler.inverse_transform(pred_price)

        output = pred_price

        print(output)

 
    
    #try_quote2 = web.DataReader(market_data, data_source='yahoo', start='2022-05-19', end='2022-05-19')
    #print(try_quote2['Close'])
