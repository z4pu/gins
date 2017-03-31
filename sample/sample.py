# -*- coding: utf-8 -*-
#!/usr/bin/python3
#
# source v_env/bin/activate
# cd sample
# python3 sample.py

import helpers
import requests
from lxml import html
from bs4 import BeautifulSoup
import dryscrape
import sys
import re

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
    examDetails = soup.find_all("table", class_= "standardTabelle gruen")
    for item in examDetails:
        #re.sub(r'\n\s*\n', r'\n\n', item.get_text().strip(), flags=re.M)
        print(re.sub(r'\n\s*', r'\n', item.get_text().strip(), flags=re.M))
    print('\n')
    return 0

def parse_courseInfo(soup):
    print("==========")
    print("  COURSES ")
    print("==========")
    courseDetails = soup.find_all("table", class_="kursfinder")
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
    page_count_links = soup.find_all("a",href=re.compile(r".*javascript:$('#start').*"))
    try: # Make sure there are more than one page, otherwise, set to 1.
        num_pages = int(page_count_links[-1].get_text())
    except IndexError:
        num_pages = 1

    for item in courseDetails:
        #stack = []
        #for td in item.find_all("td"):
            #stack.append(td.text.replace('\n', '').replace('\t', '').strip())
        #    stack.append(td.text.replace('Registration, ', '\n').replace('\n', '').replace('\t', '').strip())
        #print(", ".join(stack) + '\n')
        print(re.sub(r'\n\s*', r'\n', item.get_text().strip(), flags=re.M))
    print('\n')
    return 0

def js_courseInfo():
    search_term = 'dryscrape'

    # set up a web scraping session
    sess = dryscrape.Session(base_url = sites['course'])

    # we don't need images
    sess.set_attribute('auto_load_images', False)

    # visit homepage and search for a term
    sess.visit('/')
    q = sess.at_xpath('//*[@name="q"]')
    q.set(search_term)
    q.form().submit()

    # extract all links
    for link in sess.xpath('//a[@href]'):
        print(link['href'])

    # save a screenshot of the web page
    sess.render('google.png')
    print("Screenshot written to 'google.png'")
    return 0

def parse_testDaFInfo(soup):
    table1 = soup.find_all("div", id = "c3430", class_="csc-default")
    table2 = soup.find_all("div", id = "c3431", class_="csc-default")
    print("=============")
    print(" TestDAF INFO")
    print("=============")
    for item in table1:
        print(re.sub(r'\n\s*', r'\n', item.get_text().strip(), flags=re.M))
    for i in table2:
        print(re.sub(r'\n\s*', r'\n', i.get_text().strip(), flags=re.M))
    print('\n')
    return 0

def parse_registrationInfo(soup):
    courseStart = soup.find_all("div", class_="accordion_content", limit = 2)
    print("==============")
    print(" Registration ")
    print("==============")
    for item in courseStart:
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
