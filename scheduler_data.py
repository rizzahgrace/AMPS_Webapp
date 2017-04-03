#!/usr/bin/python


import schedule
import os
import time


def job():
    os.system("python getsysreading.py")
    #print 'done'

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
