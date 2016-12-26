#!/usr/bin/env python3
# coding: utf-8
    
    import json
    import urllib.request
    #import requests
    
    APPNO = 'e3538b500de44713bbe6f33a5279f185'
    APIKEY = 'baa0c2564c1c4506b2a5f46120f72b69'
    
    
    endpoint = 'https://api.push7.jp/api/v1/{}/send'.format(APPNO)
    
    
    header_send = {'Content-Type':'application/json'}
    method = 'POST'
    
    
        payload = {
                "apikey":APIKEY,
                "url":"https://210.129.63.215:8080/cgi-bin/hello.py",
                "icon":"https://210.129.63.215:8080/cgi-bin/orange_icon.jpg",
                "body":"xxx",
                "title":"orange"
                }
        
        
        json_data = json.dumps(payload,indent=4).encode("utf-8")
    
    #print("json_data:{}".format(json_data))
    
        request = urllib.request.Request(endpoint,data=json_data, method=method,headers=header_send)
    #print("request:{}".format(request))
    
    """
    with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            #print("response_body:{}".format(response_body))
    """
