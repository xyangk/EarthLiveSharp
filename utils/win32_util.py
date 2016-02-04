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


if __name__ == '__main__':
    main('E:\\RmDownloads')
