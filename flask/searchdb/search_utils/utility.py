import datetime
import time
import json
import re
import os
import xml.etree.ElementTree as ET

def convertUTCDate(sec):
    if sec == 0:
        return ''
    else:
        dt = time.localtime(sec)
        return '%d/%02d/%02d' % (dt.tm_year,dt.tm_mon,dt.tm_mday)

def convertResultJSON(json_string):

    result_json =  (json.loads(json_string))
    count = result_json[0][0]
    keys = [x[0] for x in result_json[0][1]]

    ret = {}
    ret["count"] = count[0]

    results = []
    for v in result_json[0][2:]:
        tmp_dic = {}
        for i in range(len(keys)):
            if keys[i] in ['filing_date', 'pub_date', 'reg_date']:
                tmp_dic[keys[i]] = convertUTCDate(v[i])
            else:
                tmp_dic[keys[i]] = v[i]

        abs_claims = getAbstractClaims(tmp_dic['publn_nr'])

        if 'claims' in abs_claims:
            tmp_dic['claims'] = abs_claims['claims']
        if 'abstract' in abs_claims:
            tmp_dic['abstract'] = abs_claims['abstract']

        results.append(tmp_dic)
    ret["results"] = results

    return ret

def getAbstractClaims(doc_number):
    type = doc_number[-1]
    file_path = ''
    if type in ['A','T','S']:
        tmp_nr = doc_number[:-1]
        base = os.path.dirname(os.path.abspath(__file__))
        dir = '../static/XML_files/' + type + '/' + tmp_nr[0:4] + '/' + tmp_nr[4:7] + '000'
        dir += '/' + doc_number + '.xml'
        file_path = os.path.normpath(os.path.join(base, dir))

    xml_dic = xml_elements(file_path)

    return xml_dic

def xml_elements(xml_path):
    u"""指定されたpathのXMLを読み込み、画面表示用の
    JSONを返す
    """

    ret = {}
    delimiter = ","
    xml_string = ""
    with open(xml_path, encoding='eucjp') as f:
        for l in f.readlines():
            xml_string += l

    tree = ET.fromstring(xml_string) # DOM root
    t = tree.find('.//description').itertext()

    claim_element = tree.find('.//claims')
    ret['claims'] = []
    for clm in claim_element.findall('claim'):
        tmp = {}
        tmp['clm_nr'] = int(clm.attrib['num'])
        clm_text = ET.tostring(clm.find('claim-text'), encoding='UTF-8')
        clm_text = clm_text.decode()
        clm_text = clm_text.replace('<claim-text>','')
        clm_text = clm_text.replace('</claim-text>','')
        clm_text = clm_text.replace('\n','')
        tmp['clm_txt'] = clm_text

        if re.search(r'請求項[０１２３４５６７８９0123456789]', clm_text):
            tmp['ind_flg'] = 0
        else:
            tmp['ind_flg'] = 1

        ret['claims'].append(tmp)

    abst_element = tree.find('.//abstract')
    abst_text = ET.tostring(abst_element, encoding='UTF-8')
    abst_text = abst_text.decode()
    abst_text = abst_text.replace('<abstract>', '')
    abst_text = abst_text.replace('</abstract>', '')
    abst_text = abst_text.replace('\n', '')
    ret['abstract'] = abst_text

    return ret
