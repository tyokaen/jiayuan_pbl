#!/usr/bin/env python3


import sys
sys.stdout.write('Content-type: text/html; charset=UTF-8 \r\n')


################################################################################
# 				get_csv
################################################################################




import cgi
import sys
form = cgi.FieldStorage()
import cgitb
cgitb.enable()
import datetime



cd = "/home/orange/workspace/one/"

'''
date= datetime.datetime.today()
year = str(date.year) + "_"
month = str(date.month)+ "_"
day = str(date.day)+ "_"
hour = str(date.hour) + "h"
minute = str(date.minute) + "m"
second = str(date.second) +"s"
microsecond = str(date.microsecond) + "ms"
'''
#num_str = year + month + day+hour + minute + second + microsecond
#extension = ".csv"
#getName = cd + num_str + extension


if 'jiayuan' in form:
    getName = cd + form['jiayuan'].filename
    #time = form['jiayuan'].filename

    filePath = open(getName, 'wb')       
    fileData = form['jiayuan'].value
    #sys.exit(fileData.encode('utf-8'))
    filePath.write(fileData)
    filePath.close()

