#!/usr/bin/env python3
from crontab import CronTab 
    
#init cron
cron = CronTab(user='pi')
cron.remove_all()

#add new cron job
#job  = cron.new(command='/home/pi/Sensors_Database/04_timesense.py')
job  = cron.new(command='/home/pi/Sensors_Database/1_Humidity_Data_Logger.py')

#job settings
job.minute.every(1)
cron.write()
