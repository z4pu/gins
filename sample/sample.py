# -*- coding: utf-8 -*-
#!/usr/bin/python3

import helpers
import requests
from lxml import html
from bs4 import BeautifulSoup
import re

# URLS for Goethe Institut pages
sites = {'exam': 'https://www.goethe.de/ins/sg/en/spr/prf/anm.html' ,
        'course': 'https://www.goethe.de/ins/sg/en/spr/kur/gia/tup.cfm',
        'testDaF': 'http://www.testdaf.de/fuer-teilnehmende/die-pruefung/pruefungstermine/',
        'registration' : 'https://www.goethe.de/ins/sg/en/spr/kur/gia/kue.html'}

def get_info(address):
    page = requests.get(address)
    if page.status_code == 200:
        #tree = html.fromstring(page.content)
        print(address+" "+"Status ok!")
        soup = BeautifulSoup(page.text, "lxml")
        return soup
        #return tree
    elif 100 <= page.status_code <200:
        print(page.status_code)
    elif 200 < page.status_code < 400:
        print(page.status_code)
    else:
        page.raise_for_status()


def parse_examInfo(soup):
    print("==========")
    print("EXAM INFO")
    print("==========")
    examDetails = soup.find_all("table", class_= "standardTabelle gruen")
    for item in examDetails:
        #re.sub(r'\n\s*\n', r'\n\n', item.get_text().strip(), flags=re.M)
        print(re.sub(r'\n\s*\n', r'\n\n', item.get_text().strip(), flags=re.M))
    return 0

def parse_courseInfo(soup):
    print("==========")
    print("  COURSES ")
    print("==========")

    return 0

def parse_testDaFInfo(soup):
    table1 = soup.find_all("div", id = "c3430", class_="csc-default")
    table2 = soup.find_all("div", id = "c3431", class_="csc-default")
    print("=============")
    print(" TestDAF INFO")
    print("=============")
    for item in table1:
        print(re.sub(r'\n\s*\n', r'\n\n', item.get_text().strip(), flags=re.M))
    for i in table2:
        print(re.sub(r'\n\s*\n', r'\n\n', i.get_text().strip(), flags=re.M))
    #print(table2)
    return 0

def parse_registrationInfo(soup):
    courseStart = soup.find_all("div", class_="accordion_content", limit = 1)
    print("==============")
    print(" Registration ")
    print("==============")
    for item in courseStart:
        print(re.sub(r'\n\s*\n', r'\n\n', item.get_text().strip(), flags=re.M))
    return 0

def main():
    for k, v in sites.items():
        soup=get_info(v)
        if k == 'exam':
            parse_examInfo(soup)
        elif k == 'course':
            parse_courseInfo(soup)
        elif k == 'testDaF':
            parse_testDaFInfo(soup)
        elif k == 'registration':
            parse_registrationInfo(soup)
        else:
            return 0

main()
