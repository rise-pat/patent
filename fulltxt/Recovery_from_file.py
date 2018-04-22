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

if __name__ in '__main__':
    # xml用ルートディレクトリ
    xml_dirs = '/mnt/Drobo/XML_files/'
    # pdf用ルートディレクトリ
    pdf_dirs = '/mnt/Drobo/PDF_files/'
    # tiff用ルートディレクトリ
    tif_dirs = '/mnt/Drobo/TIF_files/'
    # pos用ルートディレクトリ
    pos_dirs = '/mnt/Drobo/POS_files/'

    fr = open('not_registered.txt','r')
    for l in fr:
        try:
            xml_path = l.rstrip()
            ret = archive.xml_elements(xml_path)
            pub_nr = ret['publn_nr']
            print(ret['publn_nr'])
            print(xml_path)
            dirs = ret['kind-of-jp'] + '/' + pub_nr[0:4] + '/' + pub_nr[4:7] + '000'

            #DB登録
            sql_element = archive.generate_insert_sql(ret)
            archive.register_xml_elements(sql_element)

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

            break
        except pymysql.IntegrityError:
            # キー重複エラー　ー＞　処理継続
            print("already exists: " + pub_nr)
            pass
        except (pymysql.OperationalError, pymysql.ProgrammingError, pymysql.InternalError) as error:
            # データベースエラー　エラーログファイル生成、終了　処理は継続
            except_str = traceback.format_exc()
            print(except_str)
            message = "--------------------------------------------------\n"
            message += "XML_PATH:" + xml_path + "\n"
            message += "ERROR_MSG:" + except_str + "\n"
            message += "--------------------------------------------------\n"
            f = open('publn_error_log_new.txt', 'a')
            f.write(message)
            f.close()
        except:
            except_str = traceback.format_exc()
            print(except_str)
            message = "--------------------------------------------------\n"
            message += "XML_PATH:" + xml_path + "\n"
            message += "ERROR_MSG:" + except_str + "\n"
            message += "--------------------------------------------------\n"
            f = open('publn_error_log_new.txt', 'a')
            f.write(message)
            f.close()

    fr.close()
