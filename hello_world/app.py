"""
Author: HTY
Email: 1044213317@qq.com
Date: 2023-05-22 23-30
Description: 
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'
