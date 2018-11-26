#!/usr/bin/env python3
import cgitb
import cgi
import json
import chardet
cgitb.enable()

print("Content-Type: text/plain;charset=utf-8\n")
print("Hello World!")

arguments = cgi.FieldStorage()
print(arguments)
jsonObj = {}
if 'json' not in arguments.keys():
    returnErrorMessage("No JSON found.")
else:
    jsonObj = json.loads(arguments['json'].value.decode(chardet.detect(arguments['json'].value)["encoding"]))

print(jsonObj)