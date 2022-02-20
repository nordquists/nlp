"""
1. Download all of the zips
2. Store them in an easily accessible way (perhaps directories)


Why not directories?
* Not standardized across operating systems.

"""
from collections import defaultdict
import xml.etree.ElementTree as ET
import requests
import zipfile
import os
import sys

ZIP_FILE_NAME = 'temp.zip'
XML_FILE_NAME = 'temp.xml'
CURRENT_DIRECTORY = '.'



DOWNLOAD_LINKS_FILE = ['links_2016.txt','links_2017.txt','links_2021.txt']

file_name = DOWNLOAD_LINKS_FILE[int(sys.argv[1])]

file_links = []

with open(file_name, 'r') as f:
    for line in f:
        file_links.append(line)

n = len(file_links)

for i, link in enumerate(file_links):
    sys.stdout.write("CURRENT_LINK ({:.2f}%): {}".format(i/n*100, link))
    # print("CURRENT_LINK: " + link, flush=True)
    r = requests.get(link.strip(), allow_redirects=True)
    with open(ZIP_FILE_NAME, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

    with zipfile.ZipFile(ZIP_FILE_NAME, 'r') as zip_ref:
        zip_ref.extractall()
        filename = zip_ref.namelist()[0]

    def files():
        n = 0
        while True:
            n += 1
            yield '%d.xml' % n

    file_dict = defaultdict(list)
    pat = '<?xml'
    fs = files()
    outfile = next(fs) 

    with open(filename) as infile:
        for line in infile:
            if pat not in line:
                file_dict[outfile].append(line)
            else:
                items = line.split(pat)
                file_dict[outfile].append(items[0])
                for item in items[1:]:
                    outfile = next(fs)
                    file_dict[outfile].append(pat + item)

    for file_name, lines in file_dict.items():
        try:
            tree = ET.ElementTree(ET.fromstring(''.join(lines)))

            cpc_dict = dict()

            for form in tree.getroot().findall('./us-bibliographic-data-grant/classifications-cpc/main-cpc/classification-cpc/'):
                cpc_dict[form.tag] = form.text

            for form in tree.getroot().findall('./us-bibliographic-data-grant/publication-reference/document-id/'):
                cpc_dict[form.tag] = form.text

            if not cpc_dict:
                continue

            path = './output/' + cpc_dict['section'] + '/' + cpc_dict['class'] + '/' + cpc_dict['subclass'] + '/' + cpc_dict['main-group'] + '/' + cpc_dict['subgroup'] 
            if not os.path.exists(path):
                os.makedirs(path)

            with open(path + '/' + cpc_dict['date'] + '_' + cpc_dict['doc-number'] + '.xml', 'w+') as f:
                for line in lines:
                    f.write(line)
        except:
            continue




    os.remove(ZIP_FILE_NAME)
    os.remove(filename)

