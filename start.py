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
            process = subprocess.Popen(['pkill','flask'])
            process.wait()
            process = subprocess.Popen(['python3','autorun.py'])
            process.wait()
            print("killing gitUpdaterThread")
        time.sleep(3)

def startServerThread(name):
    print("starting startServerThread")
    global upToDate
    process = subprocess.Popen(['.//start.sh'])
    while(upToDate):
        time.sleep(1)
    os.kill(process.pid,signal.SIGKILL)
    process = subprocess.Popen(['pkill','flask'])
    print("killing startServerThread")

_thread.start_new_thread(ipUpdaterThread,('ip',))
_thread.start_new_thread(startServerThread,('server',))
_thread.start_new_thread(gitUpdaterThread,('git',))
while(True):
    time.sleep(1000)
