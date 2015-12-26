#!/usr/bin/env python
__author__ = 'xiao'

import re
import urllib2
import time
import json
import os

interval = 0

def get_date():
    url_temp = 'http://himawari8.nict.go.jp/img/D531106/latest.json'
    request_temp = urllib2.Request(url_temp)
    response_temp = urllib2.urlopen(request_temp)
    data_temp = response_temp.read()

    #decode json
    json_dec = json.JSONDecoder()
    json_result = json_dec.decode(data_temp)
    date_ = str(json_result['date'])

    # get date
    pattern = re.compile(r'(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)')
    result = re.search(pattern, str(date_))
    if result:
        year = result.group(1)
        month = result.group(2)
        day = result.group(3)
        hour = result.group(4)
        minute = result.group(5)
        second = result.group(6)
    else:
        pass

    return year, month, day, hour, minute, second

def download_img(year, month, day, hour, minute, second):
    global interval

    url = "http://res.cloudinary.com/dajkskdsp/image/upload/earth/%s/%s/%s/%s_%s_%s.png" \
        % (year, month, day, hour, minute, second)
    url_2 = "https://res.cloudinary.com/dajkskdsp/image/upload/earth_live_photo_vps.png"
    request_img = urllib2.Request(url)
    request_img_2 = urllib2.Request(url_2)#substitute image.

    try:
        response_img = urllib2.urlopen(request_img)
        data_img = response_img.read()
        picname = os.path.join(os.getcwd(), "Earth.png") # pic path under the script dir
        with open(picname, 'wb') as fp:
            fp.write(data_img)
        interval = 600
        # print url
        print 'Download newest image successfully.'
           
    except:
        print "Wating server download..."    
        interval = 100
        if 'Earth.png' in os.listdir(os.getcwd()):
            print 'Use exist image.'
            picname = os.path.join(os.getcwd(), "Earth.png")            
        else:
            print 'Download substitute image.'
            response_img = urllib2.urlopen(request_img_2)
            data_img = response_img.read()
            picname = os.path.join(os.getcwd(), "Earth.png") # pic path under the script dir
            with open(picname, 'wb') as fp:
                fp.write(data_img)

    return picname

def set_wallpaper(picpath):
    os.system('gsettings set org.gnome.desktop.background picture-uri "file://%s"' % (picpath))
    os.system('gsettings set org.gnome.desktop.background picture-options "centered"')
    print 'Done.'

if __name__ == '__main__':
    while True:
        print "waiting..."
        year, month, day, hour, minute, second =  get_date()
        picname = download_img(year, month, day, hour, minute, second)
        set_wallpaper(picname)
        # print interval
        time.sleep(interval)