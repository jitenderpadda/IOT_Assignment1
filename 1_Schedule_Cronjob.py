#!/usr/bin/env python3
from crontab import CronTab

cron=CronTab(user="pi")
job=cron.new(command="/home/pi/Sensors_Database/1_Data_Logger.py")
job.minute.every(1)

cron.write()