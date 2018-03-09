# coding: utf-8
import os
import time
import re
import sys
import subprocess
import concat
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


FILE_PUBLICATION = ['JPG','JPH','JPU','JPJ']
FILE_STANDARIZED = ['PXML','UXML','PSGML','USGML']
# ダウンロード先ディレクトリ
#basedir = '/home/tomoro/ダウンロード'

def download_jplat(code, terms, basedir):
    u""" バルクダウンロードサイトよりファイルをダウンロード

    code: JPG-公開公表再公表 , JPH-登録公報、実登, JPU-登実
               PXML-特許整理標準化XML, UXML-実案整理標準化データXML
               PSGML-特許整理標準化SGML, USGML-実案整理標準化データSGML
    term: 配布の回  例) 2017-43        print(terms)
        quit()
            公報データは 2017043,  標準化データは 2017-43 の形式になる
    terms : 上記termの配列(繰り返し用)
    basedir   : 保存先ディレクトリ
    observer: ファイル監視オブザーバ watchdogモジュール

    """

    username = 'jppdl081'
    password = 'JBDyWEXT'
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : basedir}
    chromeOptions.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(executable_path='/home/tomoro/patent/download/chromedriver', chrome_options=chromeOptions)

    browser.get('https://bulkdl.j-platpat.inpit.go.jp/BD2Service/bd2/general/LoginServlet')
    text = browser.find_element_by_name('txtUserid')
    text.clear()
    text.send_keys(username)
    text = browser.find_element_by_name('txtPassword')
    text.clear()
    text.send_keys(password)
    btn = browser.find_element_by_name('btnLogin')
    btn.click()
    time.sleep(3)
    btn = browser.find_element_by_name('btnAgree')
    btn.click()

    for term in terms:
        elements = browser.find_elements_by_xpath('//*[@id="form_bulk_ichiran"]/div/div[2]/div/table/tbody/tr')
        for element in elements:
            try:
                temp = element.find_element_by_xpath('./td[6]')
                if temp is not None:
                    temp = temp.text
                    if code in FILE_PUBLICATION:
                        m = re.match(r'('+code+'_'+term+'(-\w)*)', temp)
                        if m:
                            filename = basedir+'/'+m.group(0)+'.tar.gz'
                            btn = element.find_element_by_xpath('./td[7]/a')
                            btn.click()
                            while os.path.exists(basedir+'/'+m.group(0)+'.tar.gz') == False:
                                time.sleep(5)
                            print('download : ' + m.group(0)+'.tar.gz')
            except:
                print("Unexpected error:", sys.exc_info()[0])
                break

        #if code in FILE_PUBLICATION:
        #    pattern = code+'_'+term
        #    concat.concat(basedir, pattern)
        #    print('generate :' + pattern + '.ZIP')

    time.sleep(10)

    btn = browser.find_element_by_xpath('//*[@id="form_bulk_ichiran"]/div/div[1]/div/div/ul/li[2]/a')
    btn.click()

if __name__ in '__main__':

    code = ""
    terms = []
    print('編集対象のディレクトリを入力してください')
    basedir = input('>> ')
    print('ファイルタイプの指定：\nJPG-公開公表再公表 , JPH-登録公報、実登, JPU-登実\n '+
        'PXML-特許整理標準化XML, UXML-実案整理標準化データXML\n'+
        'PSGML-特許整理標準化SGML, USGML-実案整理標準化データSGML')
    file_type = input('>> ')

    print('配布回の指定: 例 公報データは 2017043<範囲指定可能>,  標準化データは 2017-43')
    file_range = input('>> ')

    if file_type in FILE_PUBLICATION:
        code = file_type
        if re.match(r"(\d{4})(\d{3})-(\d{4})(\d{3})", file_range):
            m = re.match(r"(\d{4})(\d{3})-(\d{4})(\d{3})", file_range)
            year = m.group(1)
            start = m.group(2)
            end = m.group(4)
            for i in range(int(start), int(end)+1):
                if not os.path.exists(basedir+'/'+ code + '_' + year+('%03d' % i)+'.ZIP'):
                    terms.append(year+('%03d' % i))
            print(terms)
        elif re.match(r"\d{7}", file_range):
            code = file_type
            terms.append(file_range)
        else:
            print('code error')
            print('file_type = ' + file_type + ': file_range = ' + file_range)
            quit()

    elif file_type in FILE_STANDARIZED:
        code = file_type
        if re.match(r"\d{4}-\d{2}", file_range):
            term = file_range
        else:
            print('code error')
            print('file_type = ' + file_type + ': file_range = ' + file_range)
            quit()
    else:
        print('FILETYPE ERROR')
        quit()

    download_jplat(code, terms, basedir)
