# -*- coding: utf-8 -*-
#!/usr/bin/python3
#
# source v_env/bin/activate
# cd sample
# python3 -m pdb sample.py

import helpers
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

from lxml import html
from bs4 import BeautifulSoup
import dryscrape
import sys
import re
import pdb
import time

# http://dryscrape.readthedocs.io/en/latest/usage.html#first-demonstration
if 'linux' in sys.platform:
    # start xvfb in case no X is running. Make sure xvfb
    # is installed, otherwise this won't work!
    dryscrape.start_xvfb()


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
    table = soup.find('tbody')
    for row in table.find_all('tr'):
        for cell in row.find_all('td'):
            print(re.sub(r'\n\s*', r'\n', cell.get_text().strip(), flags=re.M))
    print('\n')
    return 0



def get_table_results(driver):
    table = driver.find_element_by_tag_name("tbody")
    for row in table.find_elements_by_tag_name('tr'):
        for cell in row.find_elements_by_tag_name('td'):
            print(re.sub(r'\n\s*', r'\n', cell.text, flags=re.M))


def parse_courseInfo(soup):
    print("===========")
    print("  COURSES ")
    print("===========")
    # Page is not possible to scrape without Selenium. Because Javascript.
    driver = webdriver.Firefox(executable_path='/usr/local/src/geckodriver') # Instantiate a webdriver object
    driver.get(sites['course']) # Go to page

    # initial wait for results
    WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "aktuelleSeite"), "1"))

    while True:
    # print current page number
        page_number = int(driver.find_element_by_class_name("aktuelleSeite").text)
        print ("----------")
        print("  Page #" + str(page_number))
        print ("---------")

        get_table_results(driver)

        try:
            next_link = driver.find_element_by_link_text(str(page_number+1))
            next_link.click()
            time.sleep(2)  # TODO: fix?
            # wait for results to load
            WebDriverWait(driver, 10).until(EC.staleness_of(next_link))
        except:
            print("---------------")
            print("End of results")
            break
    driver.close()
    return 0



def parse_testDaFInfo(soup):
    table1 = soup.find("div", id = "c3430", class_="csc-default")
    table2 = soup.find("div", id = "c3431", class_="csc-default")
    print("=============")
    print(" TestDAF INFO")
    print("=============")
    for row in table1.find_all('tr'):
        for cell in row.find_all('td'):
            print(re.sub(r'\n\s*', r'\n', cell.get_text().strip(), flags=re.M))
    for row in table2.find_all('tr'):
        for cell in row.find_all('td'):
            print(re.sub(r'\n\s*', r'\n', cell.get_text().strip(), flags=re.M))
    print('\n')
    return 0

def parse_registrationInfo(soup):
    table = soup.find_all("div", class_="accordion_content", limit = 2)
    print("==============")
    print(" Registration ")
    print("==============")
    for item in table:
        print(re.sub(r'\n\s*', r'\n', item.get_text().strip(), flags=re.M))
        print('\n')
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
