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


FILE_PUBLICATION = ['JPG','JPH','JPU']
FILE_STANDARIZED = ['PXML','UXML','PSGML','USGML']
# ダウンロード先ディレクトリ
BASEDIR = '/home/tomoro/ダウンロード'


def download_jplat(code, terms):
    u""" バルクダウンロードサイトよりファイルをダウンロード

    code: JPG-公開公表再公表 , JPH-登録公報、実登, JPU-登実
               PXML-特許整理標準化XML, UXML-実案整理標準化データXML
               PSGML-特許整理標準化SGML, USGML-実案整理標準化データSGML
    term: 配布の回  例) 2017-43        print(terms)
        quit()
            公報データは 2017043,  標準化データは 2017-43 の形式になる
    terms : 上記termの配列(繰り返し用)
    observer: ファイル監視オブザーバ watchdogモジュール

    """

    username = 'jppdl081'
    password = 'JBDyWEXT'

    browser = webdriver.Chrome(executable_path='/home/tomoro/patent/download/chromedriver')

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
                        m = re.match(r'('+code+'_'+term+'-\w)', temp)
                        if m:
                            filename = BASEDIR+'/'+m.group(0)+'.tar.gz'
                            btn = element.find_element_by_xpath('./td[7]/a')
                            btn.click()
                            while os.path.exists(BASEDIR+'/'+m.group(0)+'.tar.gz') == False:
                                time.sleep(5)
                            print('download : ' + m.group(0)+'.tar.gz')
            except:
                print("Unexpected error:", sys.exc_info()[0])
                break

        #if code in FILE_PUBLICATION:
        #    pattern = code+'_'+term
        #    concat.concat(BASEDIR, pattern)
        #    print('generate :' + pattern + '.ZIP')

    time.sleep(10)

    btn = browser.find_element_by_xpath('//*[@id="form_bulk_ichiran"]/div/div[1]/div/div/ul/li[2]/a')
    btn.click()

if __name__ in '__main__':

    code = ""
    terms = []
    # ファイルタイプと配布回の指定
    argvs = sys.argv
    if len(argvs) != 3:
        print('command option error')
        quit()

    if argvs[1] in FILE_PUBLICATION:
        code = argvs[1]
        if re.match(r"(\d{4})(\d{3})-(\d{4})(\d{3})", argvs[2]):
            m = re.match(r"(\d{4})(\d{3})-(\d{4})(\d{3})", argvs[2])
            year = m.group(1)
            start = m.group(2)
            end = m.group(4)
            print(range(int(start), int(end)+1))
            for i in range(int(start), int(end)+1):
                if not os.path.exists(BASEDIR+'/'+ code + '_' + year+('%03d' % i)+'.ZIP'):
                    terms.append(year+('%03d' % i))
            print(terms)
        elif re.match(r"\d{7}", argvs[2]):
            code = argvs[1]
            terms.append(argvs[2])
        else:
            print('code error')
            print('argv[1] = ' + argvs[1] + ': argv[2] = ' + argvs[2])
            quit()

    elif argvs[1] in FILE_STANDARIZED:
        code = argvs[1]
        if re.match(r"\d{4}-\d{2}", argvs[2]):
            term = argvs[2]
        else:
            print('code error')
            print('argv[1] = ' + argvs[1] + ': argv[2] = ' + argvs[2])
            quit()
    else:
        print('FILETYPE ERROR')
        quit()

    download_jplat(code, terms)
