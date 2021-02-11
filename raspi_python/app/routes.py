from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app import app
from app.models import User, Task
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import TaskForm

from werkzeug.urls import url_parse

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/CONNECT',  methods=['POST'])
def connect():
    print("CONNECT")
    response = make_response(redirect(url_for('index')))
    return(response) 


'''
Home the drawbot

This calls G28 on serial
'''
@app.route('/HOME',  methods=['POST'])
def homing():
    print("HOMING")
    response = make_response(redirect(url_for('index')))
    return(response) 




@app.route('/COMMAND/<changepin>', methods=['POST'])
def reroute(changepin):

    changePin = int(changepin) #cast changepin to an int
    if changePin == 1:
        print("1")
    elif changePin == 2:
        print("2")
    elif changePin == 3:
        print("3")
    elif changePin == 4:
        print("4")
    else:
        print("STOP")
    response = make_response(redirect(url_for('index')))
    return(response)