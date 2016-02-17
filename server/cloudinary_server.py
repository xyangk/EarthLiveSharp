#!/usr/bin/env python

from __future__ import print_function
import re
import urllib2
import time
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api

__author__ = 'xiao'

cloudinary.config(
        cloud_name="lniwn",
        api_key="594167573281198",
        api_secret="SGfO7imfZHq4dDRX9mcJub-NNOA"
)


def get_url():
    url_temp = 'http://himawari8.nict.go.jp/img/D531106/latest.json'
    request_temp = urllib2.Request(url_temp)
    response_temp = urllib2.urlopen(request_temp)
    data_temp = response_temp.read()

    # decode json
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

    # Download picture
    url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/{0:s}/{1:s}/{2:s}/{3:s}{4:s}{5:s}_0_0.png" \
        .format(year, month, day, hour, minute, second)
    # return url
    return url, year, month, day, hour, minute, second


def upload_img(url, public_id, folder):
    return cloudinary.uploader.upload(url, public_id=public_id, folder=folder)


def list_all(type=None):
    return cloudinary.api.resources(type=type)


def delete_by_prefix(prefix):
    return cloudinary.api.delete_resources_by_prefix(prefix)


def delete_by_type(type):
    return cloudinary.api.delete_all_resources(type=type)


def get_usage():
    return cloudinary.api.usage()


def main():
    url, year, month, day, hour, minute, second = get_url()
    public_id = "%s/%s/%s/%s_%s_%s" % (year, month, day, hour, minute, second)
    response = upload_img(url, public_id, 'earth/himawari8')
    print(response)
    with open('latest.json', 'w') as fp:
        json.dump(response, fp, sort_keys=True, indent=4, separators=(',', ':'))

    import qiniu_server
    print(qiniu_server.upload_data('wallpaper/himawari8/latest.json', json.dumps(response)))
    # cloudinary.uploader.upload('latest.json', folder='earth/himawari8')


if __name__ == '__main__':
    while True:
        main()
        time.sleep(600)
