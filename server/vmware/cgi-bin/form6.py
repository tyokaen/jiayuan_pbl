#!/usr/bin/env python3

print('Content-type: text/html; charset=UTF-8 \n')


import cgi
import sys
import os
#print(os.getcwd())

form = cgi.FieldStorage()
import cgitb
cgitb.enable()



import datetime
save_dir = ['movie']
#save_dirPath = str(os.getcwd()).rsplit('/',1)[0]+"/" + save_dir[0] + "/"
#save_dirPath = str(os.getcwd()) + "/" + save_dir[0] + "/"
save_dirPath = "/home/orange/workspace/" + save_dir[0] + "/"
#save_dirPath = "http://130.158.80.39:8080/" + save_dir[0] +"/"

#sys.exit(save_dirPath)



if 'jiayuan' in form:
    videoName = form['jiayuan'].filename
    videoPath = save_dirPath + videoName
  #  sys.exit(videoPath)
    video = open(videoPath,'wb')
    videoData = form['jiayuan'].value
    video.write(videoData)
    video.close()
    
    settingPath = save_dirPath + "setting.txt"
    settingName = open(settingPath,'w')
    settingName.write(videoName)
    settingName.close()
    #sys.exit(settingPath)

                                    
    #print(videoPath)
    dirPath = "http://130.158.80.39:8080/" + save_dir[0] + "/"
    #fileName = "orange.mp4"
    video_distributionPath = dirPath + videoName
    #sys.exit(video_distributionPath)

    #videoPath = "http://210.129.63.215:8080/movie/orange.mp4"
    #print(video_distributionPath)


    html = u'''
    <!doctype html>
    <html>
    <head>
    <meta charset='utf-8'></meta>
    <title>Orange Home Security</title>
    </head>
    <body>
    <h1>Orange Home Security</h1></br>
    <video src="%s" controls>
    </video>
    </body>
    </html>
    '''

    #sys.stdout.write(html % video_distributionPath)
    print(html % video_distributionPath)
else:
    openPath = save_dirPath + "setting.txt"
    #sys.exit(str(openPath))
    settingFile = open(openPath, 'r')
    videoName = ""
    for line in settingFile:
        videoName = line
    #print(videoName)
    settingFile.close()
    video_distributionPath = "http://130.158.80.39:8080/" + save_dir[0] + "/" + videoName
    #video_distributionPath = "/home/orange/workspace/movie/" + videoName
    #print(video_distributionPath)
    #sys.exit(video_distributionPath)


    html = u'''
    <!doctype html>
    <html>
    <head>
    <meta charset='utf-8'></meta> 
    <title>Orange Home Security</title>
    </head>
    <body>
    <h1>Orange Home Security</h1></br>
    <video preload="auto" onclick="this.play()" controls>
    <source src="%s" >
    </video>
    </body>
    </html>                                                                                            
    '''
    sys.stdout.write(html % video_distributionPath)
    #print(html % video_distributionPath)
    #print(html)
