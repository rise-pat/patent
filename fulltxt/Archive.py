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

def remove_tags(element):

    tmp = re.sub(r"<.*?>", "", element)
    return re.sub(r"\s", "", tmp)

def xml_elements(xml_path):
    u"""指定されたpathのXMLを読み込み、DB登録用の
    項目を返す
    """

    delimiter = ","
    xml_string = ""
    with open(xml_path, encoding='eucjp') as f:
        for l in f.readlines():
            xml_string += l

    tree = ET.fromstring(xml_string) # DOM root
    t = tree.find('.//description').itertext()

    ret = {}
    kind = tree.get('kind-of-jp')
    ret['kind-of-jp'] = kind
    ret['appln_nr'] = tree.find('.//application-reference/document-id/doc-number').text
    ret['filing_date'] = tree.find('.//application-reference/document-id/date').text
    if tree.find('.//publication-reference/document-id/doc-number') is not None:
        if kind == 'S':
            tmp = tree.find('.//publication-reference/document-id/doc-number').text
            ret['publn_nr'] = tmp.replace('WO','') + kind
        elif kind in ['A','T']:
            ret['publn_nr'] = tree.find('.//publication-reference/document-id/doc-number').text + kind
        ret['pub_date'] = tree.find('.//publication-reference/document-id/date').text

    registar_root = tree.find('.//dates-of-public-availability')
    if registar_root is not None:
        #print ET.tostring(registar_root, encoding="utf-8")
        ret['reg_nr'] = registar_root.find('printed-with-grant/document-id/doc-number').text
        ret['reg_date'] = registar_root.find('printed-with-grant/document-id/date').text
        #print ET.tostring(registar_root, encoding="utf-8")

    ret['title'] = tree.find('.//invention-title').text

    ##### IPC
    ipc_classes = []
    ipc_root = tree.find('.//classification-ipc')
    ipc_classes.append(ipc_root.find('main-clsf').text.rstrip(' '))
    further_ipc = ipc_root.find('further-clsf')
    if further_ipc is not None:
        for f_ipc in ipc_root.iter('further-clsf'):
            ipc_classes.append(f_ipc.text.rstrip(' '))

    additional = ipc_root.find('additional-info')
    if additional is not None:
        for a_ipc in ipc_root.iter('additional-info'):
            ipc_classes.append(a_ipc.text.rstrip(' '))
    for i in range(len(ipc_classes)):
        ipc_classes[i] = ipc_classes[i][:15].replace(' ','')
    ret['clsf'] = ' '.join(ipc_classes)

    ####### FI
    fi_classes = []
    fi_root = tree.find('.//classification-national')
    fi_classes.append(fi_root.find('main-clsf').text.replace(' ',','))
    further_fi = fi_root.find('further-clsf')
    if further_fi is not None:
        for f_fi in fi_root.iter('further-clsf'):
            fi_classes.append(f_fi.text.replace(' ',','))
    ret['fi'] = ' '.join(fi_classes)

    parties = tree.find('.//parties')
    applicants = []
    for item in parties.iter('applicant'):
        applicants.append(remove_tags(item.find('.//addressbook/name').text))
    ret['applicants'] = ' '.join(applicants)

    inventors = []
    for item in parties.iter('inventor'):
        inventors.append(remove_tags(item.find('.//addressbook/name').text))
    ret['inventors'] = ' '.join(inventors)

    if parties.find('.//agent') is not None:
        agents = []
        for item in parties.iter('agent'):
            agents.append(remove_tags(item.find('.//addressbook/name').text))
            ret['attorneys'] = ' '.join(agents)

    claim_element = tree.find('.//claims')
    ret['claims'] = ""
    for text in claim_element.findall('.//claim-text'):
         ret['claims'] += re.sub(r'\n+', '', ''.join(text.itertext()))

    descriptino_element = tree.find('.//description')
    ret['description'] = re.sub(r'\n+', '', ''.join(descriptino_element.itertext()))

    abst_element = tree.find('.//abstract')
    ret['abstract'] = re.sub(r'\n+', '', ''.join(abst_element.itertext()))

    if tree.find('.//bibliographic-data/{http://www.jpo.go.jp}corrected-publication-date') is not None:
        ret['corrected-publication-date'] = tree.find('bibliographic-data/{http://www.jpo.go.jp}corrected-publication-date').text

    if tree.find('.//{http://www.jpo.go.jp}:overflow') is not None:
        ret['overflow'] = tree.find('.//{http://www.jpo.go.jp}:overflow')

    return ret

def generate_insert_sql(dictionary):
    """ dictionary に含まれた要素によってインサート文とパラメータリストを生成
    """

    dictionary.pop('kind-of-jp')
    columns = list(dictionary.keys())
    params = list(dictionary.values())

    sql = "insert into publn_data (id," + ','.join(columns) + ") values (NULL,"
    sql += ','.join(['%s' for i in range(len(params))])
    sql += ")"

    return [sql, params]

def register_xml_elements(sql_element):
    """ 取得したxml要素でsqlにインサート
    """
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
    stmt.execute(sql_element[0], sql_element[1])
    stmt.close()

def error_log(xml_path, message):
    """ xml解析エラーのDBへの記録 """
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

    sql = "insert into publn_error (xml_path, message) values (%s, %s)"

    stmt.execute(sql, [xml_path, message])
    stmt.close()



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
                ret = xml_elements(xml_path)
                # 再公表は発行日を再公表日に書き換え
                if 'corrected-publication-dat' in ret:
                    ret['pub_date'] = ret['corrected-publication-date']
                pub_nr = ret['publn_nr']
                print(pub_nr)
                print(xml_path)
                dirs = ret['kind-of-jp'] + '/' + pub_nr[0:4] + '/' + pub_nr[4:7] + '000'

                #DB登録
                sql_element = generate_insert_sql(ret)
                register_xml_elements(sql_element)
            except pymysql.IntegrityError:
                # キー重複エラー　ー＞　DBログ記録後継続
                except_str = traceback.format_exc()
                error_log(xml_path, except_str)
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
                except_str = traceback.format_exc()
                print(except_str)
                message = "--------------------------------------------------\n"
                message += "XML_PATH:" + xml_path + "\n"
                message += "ERROR_MSG:" + except_str + "\n"
                message += "--------------------------------------------------\n"
                error_log(xml_path, except_str)

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
