#!/usr/bin/env python
__auther__ = 'xiao'

import re
import urllib2
import time
import json
import subprocess

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
    url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/thumbnail/550/"+ \
        year+"/"+month+"/"+day+"/"+hour+minute+second+"_0_0.png"
    request_img = urllib2.Request(url)
    response_img = urllib2.urlopen(request_img)
    data_img = response_img.read()
    picname = '/Users/xiao/Pictures/Earth.png'# change this path
    with open(picname, 'wb') as fp:
        fp.write(data_img)

    return picname

def set_wallpaper():
    picpath = download_img()
    time.sleep(30)#wait for download
    script = """/usr/bin/osascript<<END
                tell application "Finder"
                set desktop picture to POSIX file "%s"
                end tell
                END"""
    subprocess.call(script%picpath, shell=True)
    print 'Done.'

if __name__ == '__main__':
    while True:
        set_wallpaper()
        time.sleep(600)
