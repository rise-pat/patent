#coding:utf-8
import re
import Archive as archive

fr = open('publn_error_log.txt','r')
fw = open('not_registered.txt', 'w', encoding='utf-8')

path = r"(\/mnt\/Drobo\/JPO\/2\.公報情報\/公開公報情報\/JPG_.+\/JPG_\d+\/DOCUMENT\/)([ATS])(\/.+\/)(\d+\.xml)"
#path = r"XML_PATH:.+"
pattern = re.compile(path)

nr_list = []
for l in fr:
    m = re.search(pattern,l)
    if m:
        file_path = m.group(0)
        fw.writelines(file_path+'\n')

#for line in nr_list:
    #fw.writelines(line+'\n')

fr.close()
fw.close
