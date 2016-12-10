# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName:      subtitle.py
# Author:        binss
# Create:        2016-08-15 18:25:27
# Description:   No Description
#

import os
import argparse
import hashlib
import urllib
import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')
API_URL = 'https://www.shooter.cn/api/subapi.php'


def getFileSize(path):
    if isinstance(filestring_or_fileobj, basestring):
        file_stat = os.stat(filestring_or_fileobj)
        return file_stat.st_size
    stat = os.fstat(filestring_or_fileobj.fileno())
    return stat.st_size



def svplayerHash(path):
    # 算法
    # 取文件第4k位置，再根据floor( 文件总长度/3 )计算，取中间2处，再取文件结尾倒数第8k的位置， 4个位置各取4k区块做md5。共得到4个md5值
    with open(path, 'rb') as fp:
        total_size = os.fstat(fp.fileno()).st_size
        if total_size < 8192:
            return
        seek_positions = [4096, total_size / 3 * 2, total_size / 3, total_size - 8192]
        hash_result = []
        for pos in seek_positions:
            fp.seek(pos, 0)
            data = fp.read(4096)
            m = hashlib.md5(data)
            hash_result.append(m.hexdigest())
        return ';'.join(hash_result)
    return


def downloadSubtitle(url, filedir, filename, language, ext):
    response = urllib2.urlopen(url)
    if response.code == 200:
        filename, _ = os.path.splitext(filename)
        subfilename = '%s.%s.%s' % (filename, language.lower(), ext)
        subfilepath = os.path.join(filedir, subfilename)
        if os.path.exists(subfilepath):
            return 'Subtitle exist'
        with open(subfilepath, 'wb') as fp:
            fp.write(response.read())
    return


def getSubtitle(path, language='Chn'):
    filehash = svplayerHash(path)
    if not filehash:
        return 'Cannot hash the file'

    filedir, filename = os.path.split(path)

    payload = {'filehash': filehash,
               'pathinfo': filename,
               'format': 'json',
               'lang': language}

    data = urllib.urlencode(payload)
    request = urllib2.Request(API_URL, data)
    try:
        response = urllib2.urlopen(request)
        result = response.read()
        if result == '\xff':
            return 'Cannot find subtitile'
        subtitles = json.loads(result)
        if subtitles:
            # 只取第一个结果
            subtitle = subtitles[0]
            subfiles = subtitle['Files']
            # 优先ASS
            for subfile in subfiles:
                if subfile['Ext'] == 'ass':
                    result = downloadSubtitle(subfile['Link'], filedir, filename, language, subfile['Ext'])
                    return result
            result = downloadSubtitle(subfiles[0]['Link'], filedir, filename, language, subfiles[0]['Ext'])
            return result
    except Exception as e:
        return 'Subtitile download failed because of exception'



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="The directory contains vedio files")
    parser.add_argument('--lang', choices=['Chn', 'Eng'], dest='language', default='Chn',
                        help="choose the language of subtitle, it only can be 'Chn' or 'Eng'. Default: Chn")
    args = parser.parse_args()
    path = args.path
    language = args.language

    result = getSubtitle(path, language)
    if result:
        print result
        sys.exit(1)


if __name__ == '__main__':
    main()
