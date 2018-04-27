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

    xml_path = "/mnt/Drobo/JPO/2.公報情報/公開公報情報/JPG_2017-/JPG_2017001/DOCUMENT/A/2017000001/2017000001/2017000001/2017000001.xml"

    ret = archive.xml_elements(xml_path)
    pub_nr = ret['publn_nr']
    print("pub_date = " + ret['pub_date'])

    if 'corrected-publication-date' in ret:
        ret['pub_date'] = ret['corrected-publication-date']
    print("pub_date(re) = " + ret['pub_date'])

    print("publn_nr = " + ret['publn_nr'])
