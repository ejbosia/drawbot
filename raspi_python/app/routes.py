from flask import render_template, flash, redirect, url_for, request, make_response

from app import app
from app.forms import GcodeForm


from werkzeug.utils import secure_filename

from werkzeug.urls import url_parse

import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect',  methods=['POST'])
def connect():
    print("CONNECT")
    response = make_response(redirect(url_for('index')))
    return(response) 


'''
Home the drawbot

This calls G28 on serial
'''
@app.route('/home',  methods=['POST'])
def homing():
    print("HOMING")
    response = make_response(redirect(url_for('index')))
    return(response) 


@app.route('/command/<changepin>', methods=['POST'])
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



@app.route('/run')
def upload():
    return render_template('upload.html')
	

@app.route('/upload')
def upload():
    return render_template('upload.html')
	

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    def allowed_filename(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    if request.method == 'POST':
        
        if 'file' not in request.files:
            flash("No file part?")
            return redirect('/upload')
        
        f = request.files['file']

        if f.filename == '':
            flash('No selected file')
            return redirect('/upload')
        
        if f and allowed_filename(f.filename):            
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        
        else:
            flash('Invalid file type')
            return redirect('/upload')
        
