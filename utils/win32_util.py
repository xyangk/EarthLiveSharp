#! python2
# -*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from watchdog.events import RegexMatchingEventHandler
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer
import time
import logging
import os
import ctypes
import ctypes.wintypes
from PIL import Image

# global define
_ChangeCallback = None   # _ChangeCallback(change_path, event_name)
# ------------------------


class ImageChangeEventHandler(RegexMatchingEventHandler):
    def __init__(self, ignore_regexes=[], ignore_directories=True):
        super(ImageChangeEventHandler, self).__init__(
            [r".+\.bmp$", r".+\.png$", r".+\.jpg$", r".+\.jpeg$", r".+\.gif$"],
            ignore_regexes, ignore_directories, False)

    def on_deleted(self, event):
        if event.is_directory:
            return super(ImageChangeEventHandler, self).on_deleted(event)
        if callable(_ChangeCallback):
            _ChangeCallback(event.src_path, 'on_deleted')

    def on_moved(self, event):
        if event.is_directory:
            super(ImageChangeEventHandler, self).on_moved(event)
        if callable(_ChangeCallback):
            _ChangeCallback((event.src_path, event.dest_path), 'on_moved')

    def on_modified(self, event):
        if event.is_directory:
            return super(ImageChangeEventHandler, self).on_modified(event)
        # if callable(_ChangeCallback):
        #     _ChangeCallback(event.src_path, 'on_modified')

    def on_created(self, event):
        if event.is_directory:
            return super(ImageChangeEventHandler, self).on_created(event)
        if callable(_ChangeCallback):
            _ChangeCallback(event.src_path, 'on_created')


def main(watch_path):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    os.makedirs(watch_path) if not os.path.exists(watch_path) else None
    dog = Observer()
    image_handler = ImageChangeEventHandler()
    log_handler = LoggingEventHandler()
    watch_instance = dog.schedule(image_handler, watch_path)
    dog.add_handler_for_watch(log_handler, watch_instance)
    dog.start()
    print(u'watching', watch_path, u',interrupt watching with Ctrl + C')
    wait_interrupt()
    dog.stop()
    dog.join()


def register_change_notify(callback):
    global _ChangeCallback
    _ChangeCallback = callback


def wait_interrupt():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    print('break down')


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
    main('E:\\RmDownloads')
