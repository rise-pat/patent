#!/usr/bin/env python
# -*- coding: utf-8-*-
import xml.etree.ElementTree as ET
import tarfile
import zipfile
import re
from pathlib import Path
import shutil
import os
import pymysql
import sys
import traceback
import subprocess
import getpass
import Archive as archive

if __name__ in '__main__':
    # txt用ルートディレクトリ
    txt_dirs = '/mnt/Drobo/TXT_files/'
    # img用ルートディレクトリ
    img_dirs = '/mnt/Drobo/IMG_files/'
    # pos用ルートディレクトリ
    pos_dirs = '/mnt/Drobo/POS_files/'

    print('処理対象の公報フォルダを入力')
    target_folder = input('>> ')

    print('公報種類を入力してください(A,A5,S,S5,T,T5):複数可')
    in_filetype = input('>> ')

    print('新規登録 (zipファイル未解凍？) : y/n')
    is_new = input('>> ')

    # 全文ファイル格納Dir -> 都度書き換える
    root_dir = "/mnt/Drobo/JPO/2.公報情報/公開公報情報/" + target_folder
    files = os.listdir(root_dir)
    file_list = []
    for f in files:
        #if f >= 'JPA_1998036.zip':
        #    continue
        if os.path.isdir(root_dir + '/' + f):
            #continue
            if is_new == 'n':
                # 再登録時はこちら　ディレクトリ追加
                file_list.append(root_dir + '/' + f)
        else:
            if is_new == 'y':
                file_list.append(root_dir + '/' + f)
            else:
                if re.search('\.ISO', f):
                    file_list.append(root_dir + '/' + f)

    str_f_list = sorted(file_list, reverse=True)

    for f_name in str_f_list:
        d_path = re.sub(r'\.ZIP|\.ISO|\.tar\.gz|.zip', '', f_name) + '/'
        print(f_name)
        if re.search('\.ZIP|\.tar\.gz|\.zip', f_name):
            try:
                arch_file = tarfile.open(f_name)
                arch_file.extractall(d_path)
                arch_file.close()
            except tarfile.ReadError:
                with zipfile.ZipFile(f_name) as existing_zip:
                    existing_zip.extractall(d_path)
        elif re.search('.ISO', f_name):
            os.makedirs(d_path, exist_ok=True)
            subprocess.call(('sudo mount ' + f_name + ' ' + d_path), shell=True)

        print(d_path)

        path_list = []
        for ft in in_filetype.split(','):
            tar_path = Path(d_path + 'DOCUMENT/' + ft)
            path_list += list(tar_path.glob("**/*.TXT"))

        for pl in path_list:

            try:
                xml_path = str(pl)
                print(xml_path)
                pub_nr = ''
                match = re.search(r'\/DOCUMENT\/([ATS])\/.+\/(\d{2})(\d{6})\.TXT', xml_path)
                if match:
                    type = match.group(1)
                    year = match.group(2)
                    if year >= '00' and year <= '09':
                        year = '20' + year
                    else:
                        year = '19' + year
                    pub_nr = year + match.group(3) + type
                dirs = type + '/' + pub_nr[0:4] + '/' + pub_nr[4:7] + '000'

            except:
                except_str = traceback.format_exc()
                print(except_str)
                message = "--------------------------------------------------\n"
                message += "XML_PATH:" + xml_path + "\n"
                message += "ERROR_MSG:" + except_str + "\n"
                message += "--------------------------------------------------\n"
                f = open('publn_archive_error_log.txt', 'a')
                f.write(message)
                f.close()

            # copy txt file
            os.makedirs(txt_dirs + dirs, exist_ok=True)
            target_xml = txt_dirs + dirs + '/' + pub_nr + '.txt'
            if not os.path.isfile(target_xml):
                shutil.copy(xml_path, target_xml)

            # copy xml file
            os.makedirs(img_dirs + dirs, exist_ok=True)
            target_img = img_dirs + dirs + '/' + pub_nr + '.img'
            if not os.path.isfile(target_img):
                shutil.copy(xml_path.replace('txt', 'img'), target_img)

            # copy xml file
            os.makedirs(pos_dirs + dirs, exist_ok=True)
            target_pos = pos_dirs + dirs + '/' + pub_nr + '.pos'
            if not os.path.isfile(target_pos):
                shutil.copy(xml_path.replace('txt', 'pos'), target_pos)

        #unmount ISOファイル
        if re.search('.ISO', f_name):
            subprocess.call(('sudo umount ' + d_path), shell=True)
