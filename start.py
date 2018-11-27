#!/usr/bin/env python3
import time
import subprocess
import _thread

upToDate = True

def ipUpdaterThread(name):
    while(upToDate):
        subprocess.Popen(['.//..//updateip.sh'])
        time.sleep(60)

def gitUpdaterThread(name):
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
            exit(0)
        time.sleep(60)

def startServerThread(name):
    process = subprocess.Popen(['.//start.sh'])
    while(upToDate):
        time.sleep(60)
    process.kill()

_thread.start_new_thread(ipUpdaterThread,('ip',))
_thread.start_new_thread(startServerThread,('server',))
_thread.start_new_thread(gitUpdaterThread,('git',))
while(True):
    time.sleep(1000)
