#!/usr/bin/env python
__auther__ = 'xiao'

import re
import urllib2
import time
import json
import os

def download_img():
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

    #Download picture
    # url = "https://res.cloudinary.com/dajkskdsp/image/upload/earth_live_photo_vps.png"
    url = "http://res.cloudinary.com/dajkskdsp/image/upload/%s_%s_%s_%s_%s_%s_earth_live_photo_vps.png" \
    	% (year, month, day, hour, minute, second)

    request_img = urllib2.Request(url)
    response_img = urllib2.urlopen(request_img)
    data_img = response_img.read()
    picname = '/home/xiao/Pictures/himawari8/Earth.png'#change this path
    with open(picname, 'wb') as fp:
        fp.write(data_img)

    return picname

def set_wallpaper():
    time.sleep(30)#wait for server download
    picpath = download_img()
    os.system('gsettings set org.gnome.desktop.background picture-uri "file://%s"' % (picpath))
    print 'Done.'

if __name__ == '__main__':
    while True:
        print "waiting..."
        set_wallpaper()
        time.sleep(600)
