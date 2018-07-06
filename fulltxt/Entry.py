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

    print('処理対象の年度:範囲指定2012-2015')
    in_year = input('>> ')
    target_years = []
    if re.match(r'\d{4}-\d{4}',in_year):
        temp = in_year.split('-')
        target_years = range(int(temp[0]),int(temp[1])+1)
    elif re.match(r'\d{4}', in_year):
        target_years = [in_year]
    else:
        print('入力が不正です')
        sys.exit()

    print('公報種類を入力してください(A,A5,S,S5,T,T5)')
    in_filetype = input('>> ')
    if in_filetype not in ['A','A5','S','S5','T','T5']:
        print('入力が不正です')
        sys.exit()

    for y in target_years:
        target_year = str(y)
        root_dir = "/mnt/Drobo/XML_files/" + in_filetype + "/" +  target_year
        files = os.listdir(root_dir)
        file_list = files

        str_f_list = sorted(file_list, reverse=True)

        for f_name in str_f_list:
            print(f_name)
            tar_path = Path(root_dir + "/" + f_name)
            path_list = list(tar_path.glob("**/*.xml"))

            for pl in path_list:

                try:
                    xml_path = str(pl)
                    ret = archive.xml_elements(xml_path)
                    pub_nr = ret['publn_nr']
                    print(pub_nr)
                    print(xml_path)

                    #DB登録
                    sql_element = archive.generate_insert_sql(ret)
                    archive.register_xml_elements(sql_element)
                except (pymysql.IntegrityError, pymysql.err.IntegrityError):
                    print('already exist')
                    continue
                except (pymysql.OperationalError, pymysql.ProgrammingError, pymysql.InternalError) as error:
                    # データベースエラー　エラーログファイル生成、終了　処理は継続
                    except_str = traceback.format_exc()
                    print(except_str)
                    message = "--------------------------------------------------\n"
                    message += "XML_PATH:" + xml_path + "\n"
                    message += "ERROR_MSG:" + except_str + "\n"
                    message += "--------------------------------------------------\n"
                    f = open('publn_error_log.txt', 'a')
                    f.write(message)
                    f.close()
                except:
                    # データベースエラー　エラーログファイル生成、終了　処理は継続
                    except_str = traceback.format_exc()
                    print(except_str)
                    message = "--------------------------------------------------\n"
                    message += "XML_PATH:" + xml_path + "\n"
                    message += "ERROR_MSG:" + except_str + "\n"
                    message += "--------------------------------------------------\n"
                    f = open('publn_error_log.txt', 'a')
                    f.write(message)
                    f.close()
                    sys.exit()
