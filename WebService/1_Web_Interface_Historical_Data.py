#!/usr/bin/env python3
import os
import io
import sqlite3
from datetime import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)
from sense_hat import SenseHat

app = Flask(__name__)

'''Uncomment if you dont want to see console print out'''
#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
numRows=0

def getData():
	conn=sqlite3.connect('/home/pi/Sensors_Database/sensehat.db')
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM Sensor_Data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[3])
		temp = row[1]
		hum = row[2]
	conn.close()
	return time, temp, hum

def getHistData ():
	conn=sqlite3.connect('/home/pi/Sensors_Database/sensehat.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM Sensor_Data ORDER BY timestamp DESC")
	data = curs.fetchall()
	global numRows
	numRows=len(data)
	times = []
	temps = []
	hums = []
	for row in reversed(data):
		print(row)
		times.append(row[3])
		temps.append(round(row[1]))
		hums.append(row[2])
	return times, temps, hums
# main route 
@app.route("/")
def index():	
	time, temp, hum = getData()
	templateData = {
		'time': time,
		'temp': temp,
		'hum': hum
	}
	return render_template('index.html', **templateData)

@app.route('/plot/temp')	
def plot_temp():
	times, temps, hums = getHistData()
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numRows)
	print(xs)
	print(ys)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

@app.route('/plot/hum')
def plot_hum():
	times, temps, hums = getHistData()
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numRows)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
	host = os.popen('hostname -I').read()
	app.run(host=host, port=80, debug=False)
