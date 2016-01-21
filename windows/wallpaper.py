#! python2

from __future__ import print_function
import re
import urllib2
import time
import json
import os
import ctypes
import ctypes.wintypes
from PIL import Image

__author__ = 'lniwn'
__mail__ = 'lniwn@live.com'

interval = 60*11
ACCOUNT_NAME = ''


def get_date():
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

    return year, month, day, hour, minute, second


def download_img(year, month, day, hour, minute, second):
    global interval

    url = "http://res.cloudinary.com/{0:s}/image/fetch/http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/{1:s}/{2:s}/{3:s}/{4:s}{5:s}{6:s}_0_0.png" \
        .format(ACCOUNT_NAME, year, month, day, hour, minute, second)
    url_2 = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/{0:s}/{1:s}/{2:s}/{3:s}{4:s}{5:s}_0_0.png" \
            .format(year, month, day, hour, minute, second)

    request_img = urllib2.Request(url)
    request_img_2 = urllib2.Request(url_2)  # origin image.

    try:
        response_img = urllib2.urlopen(request_img)
        data_img = response_img.read()
        picname = os.path.join(os.getcwd(), "Earth.png")  # pic path under the script dir
        with open(picname, 'wb') as fp:
            fp.write(data_img)
        # interval = 600
        # print url
        print('Download newest image successfully.')

    except:
        print("Wating server download...")
        # interval = 100
        if 'Earth.png' in os.listdir(os.getcwd()):
            print('Use exist image.')
            picname = os.path.join(os.getcwd(), "Earth.png")
        else:
            print('Download substitute image.')
            response_img = urllib2.urlopen(request_img_2)
            data_img = response_img.read()
            picname = os.path.join(os.getcwd(), "Earth.png")  # pic path under the script dir
            with open(picname, 'wb') as fp:
                fp.write(data_img)

    return picname


def set_wallpaper(picpath):
    bg_img = scale_image(picpath)
    bmp_path = os.path.splitext(picpath)[0] + '.bmp'
    bg_img.save(bmp_path)
    done = ctypes.windll.user32.SystemParametersInfoA(0x0014, 0, ctypes.create_string_buffer(bmp_path), 1)
    print('set wallpaper', 'successfully' if done else 'failed')


def scale_image(raw_img):
    bg_size = get_screen_size()
    bg_img = Image.new('RGB', bg_size, 'black')
    im = Image.open(raw_img)
    raw_size = im.size
    o_x = (bg_size[0] - raw_size[0]) // 2
    o_y = (bg_size[1] - raw_size[1]) // 2
    bg_img.paste(im, (o_x, o_y))
    return bg_img


def get_screen_size():
    w = ctypes.windll.user32.GetSystemMetrics(0)
    h = ctypes.windll.user32.GetSystemMetrics(1)
    return w, h


if __name__ == '__main__':
    while len(ACCOUNT_NAME) == 0:
        ACCOUNT_NAME = raw_input('please input your cloudinary account name>>>')
    while True:
        print("waiting...")
        picname = download_img(*get_date())
        set_wallpaper(picname)
        # print interval
        time.sleep(interval)
