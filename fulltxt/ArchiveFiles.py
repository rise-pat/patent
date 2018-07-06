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
    # xml用ルートディレクトリ
    xml_dirs = '/mnt/Drobo/XML_files/'
    # pdf用ルートディレクトリ
    pdf_dirs = '/mnt/Drobo/PDF_files/'
    # tiff用ルートディレクトリ
    tif_dirs = '/mnt/Drobo/TIF_files/'
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
        if f not in ['JPG_2004002.zip']:
            continue
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
        print(d_path)
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
            path_list += list(tar_path.glob("**/*.xml"))

        for pl in path_list:

            try:
                xml_path = str(pl)
                ret = archive.xml_elements(xml_path)
                # 再公表は発行日を再公表日に書き換え
                if 'corrected-publication-dat' in ret:
                    ret['pub_date'] = ret['corrected-publication-date']
                pub_nr = ret['publn_nr']
                print(pub_nr)
                print(xml_path)
                dirs = ret['type'] + '/' + pub_nr[0:4] + '/' + pub_nr[4:7] + '000'

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

            # copy xml file
            os.makedirs(xml_dirs + dirs, exist_ok=True)
            target_xml = xml_dirs + dirs + '/' + pub_nr + '.xml'
            if not os.path.isfile(target_xml):
                shutil.copy(xml_path, target_xml)

            # copy pdf file
            os.makedirs(pdf_dirs + dirs, exist_ok=True)
            target_pdf = pdf_dirs + dirs + '/' + pub_nr + '.pdf'
            if not os.path.isfile(target_pdf):
                shutil.copy(xml_path.replace('xml', 'pdf'), target_pdf)

            # copy xml file
            os.makedirs(tif_dirs + dirs, exist_ok=True)
            target_tif = tif_dirs + dirs + '/' + pub_nr + '.tif'
            if not os.path.isfile(target_tif):
                shutil.copy(xml_path.replace('xml', 'tif'), target_tif)

            # copy xml file
            os.makedirs(pos_dirs + dirs, exist_ok=True)
            target_pos = pos_dirs + dirs + '/' + pub_nr + '.pos'
            if not os.path.isfile(target_pos):
                shutil.copy(xml_path.replace('xml', 'pos'), target_pos)

        #unmount ISOファイル
        if re.search('.ISO', f_name):
            subprocess.call(('sudo umount ' + d_path), shell=True)
