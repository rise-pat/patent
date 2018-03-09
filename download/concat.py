# coding: utf-8
import os
import time
import re
import sys
import concat
import subprocess

# ダウンロード先ディレクトリ設定
#BASEDIR = '/mnt/Drobo/JPO/2.公報情報/公開公報情報/JPG_2017-'設定

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
    print('編集対象のディレクトリを入力してください')
    home_dir = input('>> ')

    print('ファイル名の指定: 例 JPG_2017036 複数の場合,区切りで入力')
    file_names = input('>> ')
    file_names = file_names.split(',')
    for file_name in file_names:
        concat(home_dir, file_name)
