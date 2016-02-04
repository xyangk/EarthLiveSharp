#! python2
# -*- coding:utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
import qiniu
import json


__author__ = 'lniwn'
__mail__ = 'lniwn@live.com'
__version = '1.0.0'
__BUCKET_NAME = 'wallpaper'


def get_keys(key_path):
    with open(key_path, 'r') as fp:
        jobj = json.load(fp, encoding='utf-8')
        return jobj['qiniu']['access_key'], jobj['qiniu']['secret_key']

q = qiniu.Auth(*get_keys('keys.json'))
bucket = qiniu.BucketManager(q)


def upload_data(key, data, params=None):
    key = _safe_encode(key)
    token = q.upload_token(__BUCKET_NAME, key)
    return qiniu.put_data(token, key, data, params=params)


def upload_file(key, local_file, mime_type, check_crc=True):
    # key = _safe_encode(key)
    # key = key.encode(encoding='ascii', errors='ignore')
    token = q.upload_token(__BUCKET_NAME, _safe_encode(key))
    return qiniu.put_file(token, key, local_file, mime_type=mime_type, check_crc=check_crc)


def fetch(url, bucket_name, key=None):
    bucket_name = _safe_encode(bucket_name)
    ret, info = bucket.fetch(url, bucket_name, key=key)
    print(info)
    print(ret)
    return ret


def move_file(bucket_name, key_src, key_dst):
    bucket_name = _safe_encode(bucket_name)
    return bucket.move(bucket_name, key_src, bucket_name, key_dst)


def _safe_encode(src):
    if isinstance(src, unicode):
        src = src.encode('utf-8')
    elif _is_encoding(src, 'utf-8'):
        pass
    elif _is_encoding(src, 'gbk'):
        src = src.decode('gbk').encode('utf-8')
    elif _is_encoding(src, 'shift_jis'):
        src = src.decode('shift_jis').encode('utf-8')
    else:
        src = src.decode('utf-8', errors='ignore')

    return src


def _is_encoding(src, encoding):
    try:
        src.decode(encoding)
    except UnicodeDecodeError:
        return False
    else:
        return True


def delete(bucket_name, key):
    return bucket.delete(_safe_encode(bucket_name), _safe_encode(key))


def file_etag(file_path):
    return qiniu.etag(file_path)


def list_all(bucket_name, prefix=None, limit=None):
    bucket_name = _safe_encode(bucket_name)
    marker = None
    eof = False
    while eof is False:
        ret, eof, info = bucket.list(bucket_name, prefix=prefix, marker=marker, limit=limit)
        marker = ret.get('marker', None)
        for item in ret['items']:
            yield item

    if eof is not True:
        raise RuntimeError('qiniu list failed')


def main():
    bucket_name = 'wallpaper'
    # fetch('http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/2016/01/27/113000_0_0.png', bucket_name)
    # upload_file('fetch_size_test', 'fetch_size_test.png', mime_type='image/png', check_crc=True)
    for item in list_all(bucket_name):
        print(item)

if __name__ == '__main__':
    main()
