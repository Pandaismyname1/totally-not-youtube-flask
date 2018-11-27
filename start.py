#!/usr/bin/env python3
import time
import subprocess
import _thread

upToDate = True

def ipUpdaterThread(name):
    print("starting ipUpdaterThread")
    global upToDate
    while(upToDate):
        subprocess.Popen(['.//..//updateip.sh'])
        time.sleep(60)
    print("killing ipUpdaterThread")

def gitUpdaterThread(name):
    print("starting gitUpdaterThread")
    global upToDate
    upToDate = True
    while(upToDate):
        process = subprocess.Popen(['git','pull'],stdout=subprocess.PIPE)
        output = str(process.stdout.readline())
        print('+'+output+'+')
        if(output != "b'Already up-to-date.\\n'"):
            print('Resetting')
            upToDate = False
            time.sleep(65)
            subprocess.Popen(['git','pull'])
            subprocess.Popen(['python3','../autorun.py'])
            print("killing gitUpdaterThread")
            exit(0)
        time.sleep(60)

def startServerThread(name):
    print("starting startServerThread")
    global upToDate
    process = subprocess.Popen(['.//start.sh'])
    while(upToDate):
        time.sleep(60)
    process.kill()
    print("killing startServerThread")

_thread.start_new_thread(ipUpdaterThread,('ip',))
_thread.start_new_thread(startServerThread,('server',))
_thread.start_new_thread(gitUpdaterThread,('git',))
while(True):
    time.sleep(1000)
