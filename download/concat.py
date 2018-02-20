# coding: utf-8
import os
import time
import re
import sys
import concat
import subprocess

# ダウンロード先ディレクトリ
BASEDIR = '/home/tomoro/ダウンロード'

def concat(basedir, filename):
    files = os.listdir(basedir)
    file_ary = []
    for file in files:
        if re.match(filename+'-\w', file):
            file_ary.append(basedir + '/' + file)
    file_ary = sorted(file_ary)
    if len(file_ary) < 2:
        return
    command = ' '.join(file_ary)
    command = 'cat ' + command + ' > ' + basedir + '/' + filename + '.ZIP'
    print(command)
    try:
        subprocess.call(command, shell=True)
    except:
        return

    for f in file_ary:
        print('rm ' + f)
        subprocess.call('rm ' + f, shell=True)


if __name__ in '__main__':

    # ファイルタイプと配布回の指定
    argvs = sys.argv
    if len(argvs) != 2:
        print('command option error')
        quit()

    concat(BASEDIR, argvs[1])
