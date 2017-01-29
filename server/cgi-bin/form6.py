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
save_dirPath = "/root/workspace/" + save_dir[0] + "/"

#print(save_dirPath)



if 'jiayuan' in form:
    videoName = form['jiayuan'].filename
    videoPath = save_dirPath + videoName
    video = open(videoPath,'wb')
    videoData = form['jiayuan'].value
    video.write(videoData)
    video.close()
    
    settingPath = save_dirPath + "setting.txt"
    settingName = open(settingPath,'w')
    settingName.write(videoName)
    settingName.close()

                                    
    #print(videoPath)
    dirPath = "http://210.129.63.215:8080/" + save_dir[0] + "/"
    #fileName = "orange.mp4"
    video_distributionPath = dirPath + videoName
    

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
    <h1><室内視聴画面></h1>
    <video src="%s" controls>
    </video>
    </body>
    </html>
    '''

    #sys.stdout.write(html % video_distributionPath)
    #print(html % video_distributionPath)
else:
    openPath = save_dirPath + "setting.txt"
    #sys.exit(str(openPath))
    settingFile = open(openPath, 'r')
    videoName = ""
    for line in settingFile:
        videoName = line
    #print(videoName)
    settingFile.close()
    video_distributionPath = "http://210.129.63.215:8080/" + save_dir[0] + "/" + videoName
    #video_distributionPath = "/root/workspace/movie/" + videoName
    #print(video_distributionPath)


    html = u'''
    <!doctype html>
    <html>
    <head>
    <meta charset='utf-8'></meta> 
    <title>Orange Home Security</title>
    </head>
    <body>
    <h1><室内視聴画面></h1>
    
    <video preload="auto" onclick="this.play()" controls>
    <source src="%s" >
    </video>
    </body>
    </html>                                                                                            
    '''
    #sys.stdout.write(html % video_distributionPath)
    print(html % video_distributionPath)
    #print(html)
