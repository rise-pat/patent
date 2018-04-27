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
import Archive as archive
import traceback
import subprocess
import getpass

def check_exists(publn_nr):
    #接続情報
    dbh = pymysql.connect(
             host='localhost',
             user='tomoro',
             password='tomo',
             db='test',
             charset='utf8',
             cursorclass=pymysql.cursors.DictCursor
        )

    stmt = dbh.cursor()

    sql = "select count(*) as cnt from publn_data where publn_nr = %s"

    stmt.execute(sql, [publn_nr])
    results = stmt.fetchall()
    return results[0]['cnt']

if __name__ in '__main__':

    print('対象年度を入力')
    in_year = input('>> ')
    print('公報種類を入力してください(A,A5,S,S5,T,T5)')
    in_filetype = input('>> ')

    # 全文ファイル格納Dir -> 都度書き換える
    root_dir = "/mnt/Drobo/JPO/2.公報情報/公開公報情報/JPG_2014001-2016070"
    files = os.listdir(root_dir)
    file_list = []
    for f in files:
        if os.path.isdir(root_dir + '/' + f):
            # 再登録時はこちら　ディレクトリ追加
            if re.match(r'JPG_'+in_year+'\d{3}',f):
                file_list.append(root_dir + '/' + f)
        else:
            if re.search('\.ISO', f):
                if re.match(r'JPG_'+in_year+'\d{3}\.ISO',f):
                    file_list.append(root_dir + '/' + f)

        #if re.search('.ZIP', f):
        #    print(f)
    #p = Path(root_dir)
    #file_list = list(p.glob("**/*.ZIP"))
    str_f_list = sorted(file_list, reverse=True)

    for f_name in str_f_list:
        d_path = re.sub(r'\.ZIP|\.ISO|\.tar\.gz|.zip', '', f_name) + '/'

        if re.search('.ISO', f_name):
            os.makedirs(d_path, exist_ok=True)
            subprocess.call(('sudo mount ' + f_name + ' ' + d_path), shell=True)

        path_list = []
        tar_path = Path(d_path + 'DOCUMENT/' + in_filetype)
        path_list += list(tar_path.glob("**/*.xml"))

        for pl in path_list:
            try:
                xml_path = str(pl)
                ret = archive.xml_elements(xml_path)
                pub_nr = ret['publn_nr']
                ret = check_exists(pub_nr)
                if ret == 0:
                    f = open('not_registered_'+in_year+'.txt', 'a')
                    f.write(xml_path+'\n')
                    f.close()
            except:
                except_str = traceback.format_exc()
                print(except_str)
                message = "--------------------------------------------------\n"
                message += "XML_PATH:" + xml_path + "\n"
                message += "ERROR_MSG:" + except_str + "\n"
                message += "--------------------------------------------------\n"
                f = open('not_registered_'+in_year+'_log.txt', 'a')
                f.write(xml_path+'\n')
                f.close()

        if re.search('.ISO', f_name):
            subprocess.call(('sudo umount ' + d_path), shell=True)
            continue
