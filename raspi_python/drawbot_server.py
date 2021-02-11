from flask import Flask, render_template
from app import app

if __name__ == "__main__":
    # app.run(debug=True, host='192.168.1.76')
    app.run(debug=True, host='127.0.0.1')