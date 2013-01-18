#!/usr/bin/python
#coding: utf-8
from flask import *
from tools import randbkg, GetLRC
app = Flask(__name__)

@app.route('/')
def index():
	bg = randbkg.get()
	return render_template('index.html',bkground=bg,url=request.url)

@app.route('/q',methods=['POST'])
def q():
	res = GetLRC.getlrc(request.form)
	return res

if __name__ == '__main__':
	app.debug = True
	app.run()
