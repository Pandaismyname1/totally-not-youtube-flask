#!/usr/bin/env python3
import time
import subprocess
import _thread
import os
import signal

upToDate = True

def ipUpdaterThread(name):
    print("starting ipUpdaterThread")
    global upToDate
    counter = 0
    while(upToDate):
        counter += 1
        if counter>60:
            subprocess.Popen(['.//..//updateip.sh'])
            counter -= 60
        time.sleep(1)
    print("killing ipUpdaterThread")

def gitUpdaterThread(name):
    print("starting gitUpdaterThread")
    global upToDate
    upToDate = True
    while(upToDate):
        process = subprocess.Popen(['git','pull'],stdout=subprocess.PIPE)
        process.wait()
        output = str(process.stdout.readline())
        print('+'+output+'+')
        if(output != "b'Already up-to-date.\\n'"):
            print('Resetting')
            upToDate = False
            time.sleep(5)
            print("killing startServerThread")
            process = subprocess.Popen(['pkill','flask'])
            process.wait()
            process = subprocess.Popen(['python3','autorun.py'])
            print("killing gitUpdaterThread")
            exit(0)
        time.sleep(3)

def startServerThread(name):
    process = subprocess.Popen(['.//start.sh'])

_thread.start_new_thread(ipUpdaterThread,('ip',))
_thread.start_new_thread(startServerThread,('server',))
_thread.start_new_thread(gitUpdaterThread,('git',))
while(True):
    time.sleep(1000)
