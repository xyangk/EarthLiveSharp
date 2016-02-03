#! python2
# -*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from utils import win32_util
from server import qiniu_server as qn
import os
from PIL import Image
import imghdr

__author__ = 'lniwn'
__mail__ = 'lniwn@live.com'


def on_image_change(img_path, event_name):
    if event_name == 'on_deleted':
        qn.delete('wallpaper', os.path.split(img_path)[1])
    elif event_name == 'on_modified':
        if not is_png(img_path):
            upload_path = to_png(img_path, '~upload.tmp')
        else:
            upload_path = img_path
        qn.upload_file(os.path.split(img_path)[1], upload_path, 'image/jpeg')
    elif event_name == 'on_created':
        if not is_png(img_path):
            upload_path = to_png(img_path, '~upload.tmp')
        else:
            upload_path = img_path
        qn.upload_file(os.path.split(img_path)[1], upload_path, 'image/jpeg')


def to_png(src_path, png_path):
    im = Image.open(src_path)
    im.save(png_path, format='JPEG')
    return os.path.abspath(png_path)


def is_png(file_path):
    return imghdr.what(file_path) == 'jpeg'


def main():
    win32_util.register_change_notify(on_image_change)
    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    win32_util.main(u'wallpaper')


if __name__ == '__main__':
    main()
