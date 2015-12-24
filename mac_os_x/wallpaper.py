#!/usr/bin/env python
#__auther__ = 'xiao'

from __future__ import division
import re
import urllib2
import time
import json
import subprocess
import os
from PIL import Image

ORIGINAL_IMG_WIDTH = 550
ORIGINAL_IMG_HEIGHT = 550


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
    url = "http://res.cloudinary.com/dajkskdsp/image/upload/earth/%s/%s/%s/%s_%s_%s.png" \
        % (year, month, day, hour, minute, second)
    url_2 = "https://res.cloudinary.com/dajkskdsp/image/upload/earth_live_photo_vps.png"
    request_img = urllib2.Request(url)
    request_img_2 = urllib2.Request(url_2)
    try:
        response_img = urllib2.urlopen(request_img)#
    except:
        print "Wating server download..."
        time.sleep(60)# delay for server update
        response_img = urllib2.urlopen(request_img_2)

    data_img = Image.open(response_img)
    scaled_img = scale_original_wallpaper(data_img)
    picname = os.path.join(os.path.split(os.path.realpath(__file__))[0], "%s_%s_%s_%s_%s_%s_Earth.png" % (year, month, day, hour, minute, second)) # pic path under the script dir

    scaled_img.save(picname)

    return picname

def scale_original_wallpaper(img):
    """ Return a scaled img. """

    size = get_desktop_size()
    bg_img = Image.new('RGB', size, 'black')

    # calculate the paste origin
    o_x = (size[0] - ORIGINAL_IMG_WIDTH) // 2
    o_y = (size[1] - ORIGINAL_IMG_HEIGHT) // 2
    bg_img.paste(img, (o_x, o_y))
    return bg_img

def get_desktop_size():
    """ Get the current desktop resolution. No more than 2K.

        Return a tuple of pixels (width, height)
    """
    from AppKit import NSScreen

    frame = NSScreen.mainScreen().frame()
    height = frame.size.height
    width = frame.size.width


    MAX_WIDTH = 2000
    MAX_HEIGHT = 2000

    if width > MAX_WIDTH or height > MAX_HEIGHT:
        if width > height:
            max = width
            ratio = max / MAX_WIDTH
        else:
            max = height
            ratio = max / MAX_HEIGHT
        width = width / ratio
        height = height / ratio

    return (int(width), int(height))



def set_wallpaper():
    picpath = download_img()
    script = """/usr/bin/osascript << END
                tell application "Finder"
                    set desktop picture to POSIX file "%s"
                end tell
END"""
    subprocess.call(script%picpath, shell=True)
    time.sleep(5) # waitting for setting wallpaper.
    if os.path.isfile(picpath):
        os.remove(picpath) # delete it after wallpaper set.
    print 'Done.'

if __name__ == '__main__':
    while True:
        print "waiting..."
        set_wallpaper()
        time.sleep(600)
