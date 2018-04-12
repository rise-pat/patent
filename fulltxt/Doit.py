#coding:utf-8
import re

fr = open('publn_error_log.txt','r')
fw = open('output.txt', 'w', encoding='utf-8')

path = r"(XML_PATH:\/mnt\/Drobo\/JPO\/2\.公報情報\/公開公報情報\/JPG_2006-/JPG_\d+)(\/.+)"
pattern = re.compile(path)

fw_list = []
for l in fr:
    m = re.match(pattern,l)
    if m:
        matched = m.group(1)
        if matched not in fw_list:
            fw_list.append(m.group(1))

for line in fw_list:
    fw.writelines(line+'\n')

fr.close()
fw.close
