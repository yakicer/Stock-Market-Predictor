from flask import Blueprint, render_template, request, flash, redirect, url_for
from requests import session
from . import user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_manager, login_user, login_required, logout_user, current_user

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
from flask_login import current_user
import yfinance as yf


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user1 = user.query.filter_by(email=email).first()
        if user1:
            if check_password_hash(user1.password, password):
                flash('Başarıyla Giriş Yapıldı!', category='success')
                login_user(user1, remember=True)
                return redirect(url_for('auth.precision')) 
                
            else:
                flash('Hatalı Parola! Lütfen Tekrar Deneyiniz.', category='error')
        else:
            flash('Böyle Email Bulunmamaktadır.', category='error')

    return render_template("log_in.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user1 = user.query.filter_by(email=email).first()

        if user1:
            flash('Girmiş olduğunuz mail adresi kullanılmaktadır!', category='error')
        elif len(email) < 1:
            flash('Lütfen tüm bilgileri eksiksiz giriniz!', category='error')
        elif 13 > len(email) > 1:
            flash('Lütfen geçerli bir email giriniz!', category='error')
        elif len(firstname) < 2:
            flash('İsim 2 karakterden uzun olmalıdır!', category='error')
        elif len(lastname) < 1:
            flash('Soyisim 1 karakterden uzun olmalıdır!', category='error')
        elif password1 != password2:
            flash('Şifreler birbiri ile eşleşmiyor!', category='error')
        elif len(password1) < 8:
            flash('Şifre en az 8 karakterden oluşmalıdır!', category='error')
        else:
            new_user = user(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password1, method='sha256'))      
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Hesap Başarıyla Oluşturuldu!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route('/precision', methods=['GET', 'POST'])
@login_required
def precision():  
     if request.method == 'POST':
        market_data = request.form['info']

        model = keras.models.load_model('website/saved_dir/modeldir')

        try_quote = web.DataReader(str(market_data), data_source='yahoo', start='2019-01-01')
        new_df = try_quote.filter(['Close'])
        lst60days = new_df[-60:].values
        scaler = MinMaxScaler(feature_range=(0,1))
        lst60days_scaled = scaler.fit_transform(lst60days)
        lst60days_scaled = scaler.transform(lst60days)


        N_test = []
        N_test.append(lst60days_scaled)
        N_test = np.array(N_test)
        N_test = np.reshape(N_test, (N_test.shape[0], N_test.shape[1], 1))
        pred_price = model.predict(N_test)
        pred_price = scaler.inverse_transform(pred_price)

        try_quote2 = web.DataReader(str(market_data), data_source='yahoo', start='2022-03-03', end='2022-03-03')
        real_df = try_quote2.filter(['Close'])
        real_df_scaled = scaler.fit_transform(real_df)
        real_df_scaled = scaler.transform(real_df)

        output2=scaler.inverse_transform(real_df_scaled)



        return render_template("precision.html", user=current_user, output = pred_price, output2=output2)
     return render_template("precision.html", user=current_user)

    

@auth.route('/graphs')
@login_required
def graphs():
    return render_template("graphs.html", user=current_user)


@auth.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)
