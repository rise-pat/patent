import re
import mojimoji

def remove_tags(element):

    tmp = re.sub(r"<.*?>", "", element)
    return re.sub(r"\s", "", tmp)

def extract_elements(txt_path):
    u"""指定されたpathのTXTを読み込み、DB登録用の
    項目を返す
    """
    ret = {}
    txt_string = ""
    with open(txt_path, encoding='eucjp') as f:
        for l in f.readlines():
            txt_string += l

    #書誌事項
    reg = re.compile('<SDO BIJ>([\s\S]+?)</SDO>')
    match = reg.search(txt_string)
    biblio = match.group(1)

    #要約
    reg = re.compile('<SDO ABJ>([\s\S]+?)</SDO>')
    match = reg.search(txt_string)
    if match:
        ret['abstract'] = remove_tags(match.group(1)).replace('(57)','')

    #請求項
    reg = re.compile('<SDO CLJ>([\s\S]+?)</SDO>')
    match = reg.search(txt_string)
    if match:
        ret['claims'] = remove_tags(match.group(1))

    #詳細な説明
    reg = re.compile('<SDO DEJ>([\s\S]+?)</SDO>')
    match = reg.search(txt_string)
    if match:
        ret['description'] = remove_tags(match.group(1))

    return ret
    while True:
        line = f.readline()

        if re.search(r'【公報種別】', line):
            match = re.search(r'【公報種別】.+（([ＡＴＳ])）', line)
            ret['type'] = mojimoji.zen_to_han(match.group(1))

        if re.search(r'【公開日】', line):
            match = re.search(r'【公開日】.+（([０-９]+)．([０-９]+)．([０-９]+)）', line)
            pub_year = mojimoji.zen_to_han(match.group(1)).zfill(4)
            pub_month = mojimoji.zen_to_han(match.group(2)).zfill(2)
            pub_day =  mojimoji.zen_to_han(match.group(3)).zfill(2)
            ret['pub_date'] =  pub_year + pub_month + pub_day
            ret['pub_year'] = pub_year
            ret['pub_month'] = pub_month

        if re.search(r'【発明の名称】', line):
            match = re.search(r'【発明の名称】(.+)', line)
            ret['title'] = match.group(1)

        if re.search(r'出願番号', line):
            match = re.search(r'【出願番号】.+（([ＰＵ])([０-９]+).([０-９]+)）', line)
            app_year = mojimoji.zen_to_han(match.group(2)).zfill(4)
            app_nb = mojimoji.zen_to_han(match.group(3)).zfill(6)
            ret['appln_nr'] = mojimoji.zen_to_han(match.group(1)) + app_year + app_nb

        if not line:
            break

    f.close()

    return ret

if __name__ in '__main__':

    test = '/mnt/Drobo/TXT_files/A/2003/107000/2003107000A.txt'
    ret = extract_elements(test)
    print(ret)
