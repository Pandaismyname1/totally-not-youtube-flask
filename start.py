#!/usr/bin/env python3
import time
import subprocess
import thread

upToDate = True

def ipUpdaterThread():
    while(upToDate):
        subprocess.Popen(['./../updateip.sh'])
        time.sleep(60)

def gitUpdaterThread():
    while(upToDate):
        process = subprocess.Popen(['git','pull'],stdout=subprocess.PIPE)
        if(process.stdout.readline() != 'Already up-to-date'):
            upToDate = False
            time.sleep(65)
            subprocess.Popen(['git','pull'])
            subprocess.Popen(['python3','../autorun.py'])
            exit(0)

def startServerThread():
    process = subprocess.Popen(['./start.sh'])
    while(upToDate):
        sleep(60)
    process.kill()

thread.start_new_thread(ipUpdaterThread)
thread.start_new_thread(startServerThread)
thread.start_new_thread(gitUpdaterThread)