#!/usr/bin/env python3

import sys
import sqlite3 as lite
from sense_hat import SenseHat

# fetch Humidity from SenseHat
def getHumidityFromSensor():
    sense= SenseHat()
    humidity= sense.get_humidity()
    print("humidity---"+str(humidity))
    return humidity

# Log Humidity to Database
def logToDatabase():
    connection= lite.connect('sensehat.db')
    cursor=connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Humidity_Data (id INTEGER PRIMARY KEY AUTOINCREMENT, value NUMERIC, timestamp DATETIME)")
    humidity=getHumidityFromSensor()
    cursor.execute("INSERT INTO Humidity_Data (timestamp, value) VALUES(datetime('now'), ?)", (humidity,))
    # Print rows on console for runtime logs
    #print("Humidity_Data -")
    for row in cursor.execute("SELECT * FROM Humidity_Data"):
        print(row)
    connection.commit()
    connection.close()

def main():
    #print("Logging Humidity")
    logToDatabase()


# Run Program
main()
