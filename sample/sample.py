# -*- coding: utf-8 -*-
#!/usr/bin/python3

import helpers
import requests
from lxml import html
from beautifulsoup4 import BeautifulSoup

# URLS for Goethe Institut pages
sites = {'exam': 'https://www.goethe.de/ins/sg/en/spr/prf/anm.html' ,
        'course': 'https://www.goethe.de/ins/sg/en/spr/kur/gia/tup.cfm',
        'testDaF': 'http://www.testdaf.de/fuer-teilnehmende/die-pruefung/pruefungstermine/',
        'registrationInfo' : 'https://www.goethe.de/ins/sg/en/spr/kur/gia/kue.html'}

def get_info(address):
    page = requests.get(address)
    if page.status_code == 200:
        tree = html.fromstring(page.content)
        print("Tree success!")
        return tree
    elif 100 <= page.status_code <200:
        print(page.status_code)
    elif 200 < page.status_code < 400:
        print(page.status_code)
    else:
        page.raise_for_status()


#def parse_examInfo():



def main():
    for k, v in sites.items():
        get_info(v)

main()
