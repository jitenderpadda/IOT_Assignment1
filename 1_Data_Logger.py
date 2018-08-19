#!/usr/bin/env python3
import sys
import sqlite3 as lite
from sense_hat import SenseHat
from push_notification import send_notification_via_pushbullet 

# fetch Sensor Data from SenseHat
def getDataFromSensor(sensorType):
    sense= SenseHat()
    sense.clear()
    if(sensorType=='Humidity'):
        humidity= sense.get_humidity()
        return round(humidity)
    elif(sensorType=='Temp'):
        temp=sense.get_temperature()
        return round(temp,1)

# Log Humidity to Database
def logToDatabase():
    connection= lite.connect('/home/pi/Sensors_Database/sensehat.db')
    cursor=connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Sensor_Data (id INTEGER PRIMARY KEY AUTOINCREMENT, temp NUMERIC, hum NUMERIC, timestamp DATETIME)")
    humidity=getDataFromSensor('Humidity')
    temp=getDataFromSensor('Temp')
    # Send Push Bullet Notification if temperature meets condition
    if(temp>20):
        send_notification_via_pushbullet("It's cold out there, less than 20C","Remember to take your sweater!")
    cursor.execute("INSERT INTO Sensor_Data (timestamp, temp, hum) VALUES(datetime('now'), (?), (?))", (temp, humidity,))
    connection.commit()
    connection.close()
    
# Main function
def main():
    sense= SenseHat()
    sense.show_message("Logging")
    logToDatabase()

# Run Program
main()