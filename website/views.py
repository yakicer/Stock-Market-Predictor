from flask import Blueprint, redirect, render_template
from flask_login import login_required,  current_user

views = Blueprint('views', __name__)


@views.route('/')
def home():
     if current_user.is_authenticated==True:
          return render_template("precision.html", user=current_user)
     else:
          return render_template("home.html", user=current_user)


@views.route('/welcome')
@login_required
def welcome():
     return render_template("welcome.html", user=current_user)