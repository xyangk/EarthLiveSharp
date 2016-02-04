#! python2
# -*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from utils import win32_util
from server import qiniu_server as qn
import os
from PIL import Image
import imghdr
import threading

__author__ = 'lniwn'
__mail__ = 'lniwn@live.com'

WALLPAPER_PATH = u"./wallpaper"
CDN_HOST = u"http://7xqd64.com1.z0.glb.clouddn.com/"


def on_image_change(img_path, event_name):
    if event_name == 'on_deleted':
        qn.delete(qn.BUCKET_NAME, os.path.split(img_path)[1])
    # elif event_name == 'on_modified':
    #     if not is_png(img_path):
    #         upload_path = to_png(img_path, '~upload.tmp')
    #     else:
    #         upload_path = img_path
    #     qn.upload_file(key_from_path(img_path), upload_path, 'image/jpeg')
    elif event_name == 'on_created':
        if not is_jpeg(img_path):
            upload_path = to_jpeg(img_path, '~upload.tmp')
        else:
            upload_path = img_path
        qn.upload_file(key_from_path(img_path), upload_path, 'image/jpeg')
        win32_util.set_wallpaper(img_path)
        # for item in result[0].items():
        #     print(item[0], item[1])
    elif event_name == 'on_moved':
        src_path = img_path[0]
        dst_path = img_path[1]
        qn.rename(qn.BUCKET_NAME, key_from_path(src_path), key_from_path(dst_path))


def key_from_path(file_path):
    file_name = os.path.split(file_path)[1]
    return file_name


def to_jpeg(src_path, png_path):
    im = Image.open(src_path)
    im.save(png_path, format='JPEG')
    return os.path.abspath(png_path)


def is_jpeg(file_path):
    return imghdr.what(file_path) == 'jpeg'


def is_image(file_path):
    try:
        img_type = imghdr.what(file_path)
    except IOError:
        return False
    else:
        return img_type in ['gif', 'jpeg', 'bmp', 'png']


def schedule(interval):
    """
    装饰器函数，用于定时执行任务
    :param interval: 定时器间隔，单位 s
    :return: None
    """
    def _schedule(func):
        def wrapper(*args):
            func(*args)
            threading.Timer(interval, wrapper, args).start()
        return wrapper
    return _schedule


@schedule(3*60)
def sync_images(folder_path):
    """
    同步本地文件夹内的图片和cdn上的图片
    :param folder_path: 本地图片文件夹路径
    :return:
    """
    cdn_cache = [i['key'] for i in qn.list_all(qn.BUCKET_NAME)]
    for item in cdn_cache:
        if os.path.exists(os.path.join(WALLPAPER_PATH, item)):
            continue
        qn.download(CDN_HOST+item, os.path.join(folder_path, item))

    for item in os.listdir(folder_path):
        file_path = os.path.join(folder_path, item)
        if is_image(file_path) and item not in cdn_cache:
            qn.upload_file(item, file_path, 'image/jpeg')


def main():
    win32_util.register_change_notify(on_image_change)
    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    sync_images(WALLPAPER_PATH)
    win32_util.main(WALLPAPER_PATH)


if __name__ == '__main__':
    main()
