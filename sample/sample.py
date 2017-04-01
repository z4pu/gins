# -*- coding: utf-8 -*-
#!/usr/bin/python3
#
# source v_env/bin/activate
# cd sample
# python3 -m pdb sample.py

import helpers
import requests
from selenium import webdriver
from lxml import html
from bs4 import BeautifulSoup
import dryscrape
import sys
import re
import pdb

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

def parse_courseInfoOld(soup):
    print("==========")
    print("  COURSES ")
    print("==========")

        # <div class="paginierung">
	#<a href="javascript:$('#start').val('0'); $('#kursfinderForm').submit()" class="icon-double-arrow-left"></a>
	#		<span class="aktuelleSeite">1</span>
	#<a href="javascript:$('#start').val('20'); $('#kursfinderForm').submit()">2</a>
	#<a href="javascript:$('#start').val('20'); $('#kursfinderForm').submit()" class="icon-double-arrow-right"></a>
    #</div>

    # https://www.goethe.de/ins/sg/en/spr/kur/gia/tup.cfm?sortorder=course_startdate+ASC&start=20&limit=20&location=&coursetype=&pace=&coursestart=&format=&level=
    # <a href="javascript:$('#start').val('20'); $('#kursfinderForm').submit()">2</a>
    # http://stackoverflow.com/questions/26497722/scrape-multiple-pages-with-beautifulsoup-and-python
    # Use regex to isolate only the links of the page numbers, the one you click on.
    links = soup.find("div", class_="paginierung")
    page_count_links = links.find_all("a",href=re.compile(r".*javascript.*"))

    try: # Make sure there are more than one page, otherwise, set to 1.
        num_pages = len(page_count_links)-1
    except IndexError:
        num_pages = 1

    # Add 1 because Python range.
    url_list = ["{}&start={}{}".format(sites['course'], str(20*page-20),
        '&limit=20&location=&coursetype=&pace=&coursestart=&format=&level=') for page in range(1, num_pages + 1)]

    # FIND COURSE DATA IN TABLE
    for url_ in url_list:
        table_new = soup.find("table", class_="kursfinder")
        for row in table_new.find_all('tr'):
            for cell in row.find_all('td'):
                print(re.sub(r'\n\s*', r'\n', cell.get_text().strip(), flags=re.M))
    print('\n')
    return 0

def parse_courseInfo(soup):
    print("==========")
    print("  COURSES ")
    print("==========")
    # Page is not possible to scrape without Selenium. Because Javascript.
    browser = webdriver.Firefox(executable_path='/usr/local/src/geckodriver') # Instantiate a webdriver object
    browser.get(sites['course']) # Go to page

    # Makes list of links
    linksList = []
    # This is the container of pagelinks on the main page
    linksContainer = browser.find_elements_by_xpath("/html/body/div/div/div/div/article/div/div/div/a")

    for link in linksContainer:
    # Now assemble list to pass to requests and beautifulsoup
        click()
        table_new = soup.find("table", class_="kursfinder")
        for row in table_new.find_all('tr'):
            for cell in row.find_all('td'):
                print(re.sub(r'\n\s*', r'\n', cell.get_text().strip(), flags=re.M))
    print('\n')



        # <div class="paginierung">
	#<a href="javascript:$('#start').val('0'); $('#kursfinderForm').submit()" class="icon-double-arrow-left"></a>
	#		<span class="aktuelleSeite">1</span>
	#<a href="javascript:$('#start').val('20'); $('#kursfinderForm').submit()">2</a>
	#<a href="javascript:$('#start').val('20'); $('#kursfinderForm').submit()" class="icon-double-arrow-right"></a>
    #</div>

    # https://www.goethe.de/ins/sg/en/spr/kur/gia/tup.cfm?sortorder=course_startdate+ASC&start=20&limit=20&location=&coursetype=&pace=&coursestart=&format=&level=
    # <a href="javascript:$('#start').val('20'); $('#kursfinderForm').submit()">2</a>
    # http://stackoverflow.com/questions/26497722/scrape-multiple-pages-with-beautifulsoup-and-python
    # Use regex to isolate only the links of the page numbers, the one you click on.

    # FIND COURSE DATA IN TABLE
    #for url_ in linksList:
    #    browser.get("{}?{}".format(sites['course'], url_) # Go to page
    #    newSoup = BeautifulSoup(browser.page_source)
    #    table_new = newSoup.find("table", class_="kursfinder")
    #    for row in table_new.find_all('tr'):
    #        for cell in row.find_all('td'):
    #            print(re.sub(r'\n\s*', r'\n', cell.get_text().strip(), flags=re.M))
    #print('\n')
    browser.close()
    return 0

def js_courseInfo():
    # Page is not possible to scrape without Selenium. Because Javascript.
    #browser = webdriver.Firefox() # Instantiate a webdriver object
    #browser.get(sites['course']) # Go to page

    # Makes list of links to get full image
    #linksList = []
    # This is the container of images on the main page
    #cards = browser.find_elements_by_class_name('image-list-link')
    #for img_src in cards:
    # Now assemble list to pass to requests and beautifulsoup
    #    linksList.append(img_src.get_attribute('href'))
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
