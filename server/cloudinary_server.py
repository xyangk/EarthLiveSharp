#!/usr/bin/env python
__author__ = 'xiao'

import re
import urllib2
import time
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
  cloud_name = "your_cloud_name",
  api_key = "your_api_key",
  api_secret = "your_api_secret"
)

def get_url():
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
    # return url
    return url, year, month, day, hour, minute, second

def upload_img():
    url, year, month, day, hour, minute, second = get_url()
    url_id = "earth/%s/%s/%s/%s_%s_%s" % (year, month, day, hour, minute, second)
    cloudinary.uploader.upload(url, public_id = url_id)

if __name__ == '__main__':
    while True:
        upload_img()
        time.sleep(600)
