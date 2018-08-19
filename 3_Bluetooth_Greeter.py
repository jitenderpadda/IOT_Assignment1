#!/usr/bin/env python3
import bluetooth
import os
import time
import sqlite3
from sense_hat import SenseHat

# Main function
def main():
    menuInput=input("Welcome to Pi Bluetooth Service\nPlease choose option number from the Menu\n1. Register a Device\n2. Search and Greet\n")
    menuInput=int(menuInput)
    if(menuInput==1):
        registerDevice()
    elif(menuInput==2):
        searchAndGreet()
    else:
        print("Invalid Input")
        main()

def registerDevice():
    connection= sqlite3.connect('/home/pi/Sensors_Database/sensehat.db')
    cursor=connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS BT_Data (id INTEGER PRIMARY KEY AUTOINCREMENT, userName TEXT, deviceName TEXT)")
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    cursor.execute("INSERT INTO BT_Data(userName, deviceName) VALUES((?), (?))", (user_name, device_name,))
    connection.commit()
    connection.close()
    print("Device Registered\n\n")
    main()
    
   
def searchAndGreet():
    while True:
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) #Sleep three seconds 
        connection=sqlite3.connect('/home/pi/Sensors_Database/sensehat.db')
        curs=connection.cursor()
        for row in curs.execute("SELECT * FROM BT_Data"):
            search(row[1], row[2])
        connection.close()
    
# Search for device based on device's name
def search(user_name, device_name):
    print("user_name->"+user_name)
    print("device_name->"+device_name)
    device_address = None
    nearby_devices = bluetooth.discover_devices()
    for mac_address in nearby_devices:
        if device_name == bluetooth.lookup_name(mac_address, timeout=5):
            device_address = mac_address
            break
    if device_address is not None:
       print("Hi {}! Your phone ({}) has the MAC address: {}".format(user_name, device_name, device_address))
       sense = SenseHat()
       temp = round(sense.get_temperature(), 1)
       sense.show_message("Hi {}! Current Temp is {}*c".format(user_name, temp), scroll_speed=0.05)
    else:
       print("Could not find target device nearby...")

#Execute program
main()
