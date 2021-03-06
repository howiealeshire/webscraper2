from bs4 import BeautifulSoup
import sys
import re
import urllib.request
import pandas as pd
import pprint
import collections
from fp.fp import FreeProxy
import requests
import time
import xlsxwriter
import xlrd
import csv
from fake_useragent import UserAgent
from os import listdir
from os.path import isfile, join, basename, dirname, exists
from os import rename, remove
from os import stat, system
import random
import math
import pickle
import dill
from datetime import datetime
from itertools import groupby
from collections import OrderedDict

GLOBAL_COUNTER = 0
GLOBAL_NO_CONTENT_COUNTER = 0
GLOBAL_P_COUNTER = 0



class Person:
    def __init__(self, bus, name_searched, loc_searched, details_url, tps_name, tps_age, birth_date,
                 curr_address, phone_nums, email_addresses, prev_addresses, possible_buses_and_addresses, bus_dates,
                 prev_address_dates, file_name=''):
        self.bus = bus
        self.name_searched = name_searched
        self.loc_searched = loc_searched
        self.details_url = details_url
        self.tps_name = tps_name
        self.tps_age = tps_age
        self.birth_date = birth_date
        self.curr_address = curr_address
        self.phone_nums = phone_nums
        self.email_addresses = email_addresses
        self.prev_addresses = prev_addresses
        self.possible_buses_and_addresses = possible_buses_and_addresses
        self.bus_dates = bus_dates
        self.prev_address_dates = prev_address_dates
        self.file_name = file_name

    def convert_bus_addresses_to_string(self, b_a):
        m_string = ""
        for elem in b_a:
            m_string += elem[0] + elem[1] + ","
        return m_string

    def __str__(self):
        separator = ","
        return self.bus \
               + "," + self.name_searched \
               + "," + self.loc_searched + \
               "," + self.details_url + "," \
               + self.tps_name + "," \
               + self.tps_age + "," \
               + self.birth_date + "," \
               + self.curr_address \
               + "," + separator.join(self.phone_nums) \
               + "," + separator.join(self.email_addresses) \
               + "," + separator.join(self.prev_addresses) \
               + "," + self.convert_bus_addresses_to_string(self.possible_buses_and_addresses)


class UrlField:
    def __init__(self, first_name, last_name, city, state):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.state = state

    def __str__(self):
        return self.first_name + "," + self.last_name + "," + self.city + "," + self.state

    def __eq__(self, other):
        if isinstance(other, UrlField):
            if self.first_name == other.first_name and self.last_name == other.last_name and self.city == other.city and self.state == other.state:
                return True
            else:
                return False


def get_names_and_locations(file_path):
    df = pd.read_excel(file_path)
    names_and_locs = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
    # names_and_locs2 = [names_and_locs[0],names_and_locs[1],names_and_locs[2],names_and_locs[3],names_and_locs[4],names_and_locs[5]]
    return names_and_locs


def get_supposed_url_from_file_num(file_num):
    f = open("/Users/howie/PycharmProjects/webscraper/venv/your_file.txt", 'r')
    lines = f.readlines()
    if (file_num < len(lines)):
        return lines[file_num]
    else:
        return None


def gen_url(first_name, last_name, city, state, rid="0x0"):
    test_url = "https://www.truepeoplesearch.com/details?name=John%20Smith&citystatezip=Atlanta%2C%20GA&rid=0x0"
    template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + last_name + "&citystatezip=" + city + "%2C%20" + state + "&rid=" + rid
    return template_url


def gen_all_urls_for_one_person(first_name, last_name, city, state, rid_list):
    url_list = []
    for rid in rid_list:
        url_list.append(
            "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + last_name + "&citystatezip=" + city + "%2C%20" + state + "&rid=" + rid)
    return url_list

def gen_urls_for_one_og(first_name,last_name,city,state,middle_name,title,rids):
    url_list = []
    for rid in rids:
        url_list.append(gen_rid_url(first_name,last_name,city,state,middle_name,title,rid))
    return url_list


def gen_rid_url(first_name, last_name, city, state,middle_name="",title="",rid=""):
    if len(city.split()) > 1:
        first_city_name = city.split()[0]
        second_city_name = city.split()[1]
        if middle_name != '' and title != '':
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + middle_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + first_city_name + "%20" + second_city_name +  ",%20" + state.strip() + "&rid=" + str(rid)
        elif middle_name == '' and title != '':
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + first_city_name + "%20" + second_city_name +  ",%20" + state.strip()  + "&rid=" + str(rid)
        elif middle_name != '' and title == '':
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + middle_name + "%20" + last_name + "&citystatezip=" + first_city_name + "%20" + second_city_name +  ",%20" + state.strip()  + "&rid=" + str(rid)
        else:
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + last_name + "&citystatezip=" +  first_city_name + "%20" + second_city_name +  ",%20" + state.strip()  + "&rid=" + str(rid)
    else:
        if middle_name != '' and title != '':
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + middle_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + city + ",%20" + state.strip()  + "&rid=" + str(rid)
        elif middle_name == '' and title != '':
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + city + ",%20" + state.strip()  + "&rid=" + str(rid)
        elif middle_name != '' and title == '':
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + middle_name + "%20" + last_name + "&citystatezip=" + city + ",%20" + state.strip()  + "&rid=" + str(rid)
        else:
            template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + last_name + "&citystatezip=" + city + ",%20" + state.strip()  + "&rid=" + str(rid)

    print("template_url")
    print(template_url.strip())
    print("end template_url")
    return template_url




def gen_url_for_num_found(first_name, last_name, city, state,middle_name="",title="",rid=""):
    if len(city.split()) > 1:
        first_city_name = city.split()[0]
        second_city_name = city.split()[1]
        if middle_name != '' and title != '':
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + middle_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + first_city_name + "%20" + second_city_name +  ",%20" + state.strip()
        elif middle_name == '' and title != '':
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + first_city_name + "%20" + second_city_name +  ",%20" + state.strip()
        elif middle_name != '' and title == '':
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + middle_name + "%20" + last_name + "&citystatezip=" + first_city_name + "%20" + second_city_name +  ",%20" + state.strip()
        else:
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + last_name + "&citystatezip=" +  first_city_name + "%20" + second_city_name +  ",%20" + state.strip()
    else:
        if middle_name != '' and title != '':
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + middle_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + city + ",%20" + state.strip()
        elif middle_name == '' and title != '':
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + last_name + "%20" + title + "%20" + "&citystatezip=" + city + ",%20" + state.strip()
        elif middle_name != '' and title == '':
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + middle_name + "%20" + last_name + "&citystatezip=" + city + ",%20" + state.strip()
        else:
            template_url = "https://www.truepeoplesearch.com/results?name=" + first_name + "%20" + last_name + "&citystatezip=" + city + ",%20" + state.strip()

    print("template_url")
    print(template_url.strip())
    print("end template_url")
    return template_url


def gen_all_urls_for_num_found(names_and_locs):
    url_list = []
    for elem in names_and_locs:
        if(len(elem) == 4):
            url = gen_url_for_num_found(elem[0], elem[1], elem[2], elem[3])
        elif(len(elem) == 5):
            url = gen_url_for_num_found(elem[0], elem[1], elem[2], elem[3],elem[4])
        elif (len(elem) == 6):
            url = gen_url_for_num_found(elem[0], elem[1], elem[2], elem[3], elem[4],elem[5])
        else:
            return ''

        url_list.append(url)
    return url_list


def empty_result_detected(soup):
    soup.body.findAll(text=re.compile('^We could not find any records for that search criteria.$'))
    pass


def get_num_results(soup):
    parent_results = soup.find('div', class_="col-10 mt-1")
    if parent_results is not None:
        text = str(parent_results.getText()).strip().split()[0]
        if text is not None:
            if text.isnumeric():
                return int(text)

    else:
        return -1

def get_num_results_from_og_page(soup):
    font = soup.find("div", text="Past Movies:").find_next_sibling("font")
    pass

def get_all_num_pages(num_result_list):
    all_num_pages = []
    for elem in num_result_list:
        all_num_pages.append(get_num_pages(elem))
    return all_num_pages


def get_num_pages(num_results):
    num_per_page = 10
    num_pages = int(num_results) / num_per_page
    if (num_pages.is_integer()):
        return num_pages
    else:
        return math.ceil(num_pages)


def get_all_rids(num_pages_list):
    rid_list = []
    for elem in num_pages_list:
        rid_list.append(get_rids(elem))
    return rid_list

def get_bad_file_url_pairs():
    mypath = "/Users/howie/PycharmProjects/webscraper/venv/html_folder"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    full_paths_list = []
    files_that_need_redownloaded = grab_all_bad_file_paths()
    print("files that must be redownloaded:")
    pp.pprint(files_that_need_redownloaded)
    for elem in onlyfiles:
        full_paths_list.append(elem)
    all_urls_and_files = open("/Users/howie/PycharmProjects/webscraper/venv/files_and_urls.txt","r").readlines()
    #pp.pprint(all_urls_and_files)
    file_url_pairs = []
    for elem in all_urls_and_files:
        #print(elem)
        url_and_file = elem.rstrip()
        url_and_file = url_and_file.split(';')
        #pp.pprint(url_and_file)
        file = url_and_file[0]

        url = url_and_file[1]
        if file in files_that_need_redownloaded:
            file_url_pairs.append((file,url))
    print("file_url pairs that are bad")
    pp.pprint(file_url_pairs)
    print("end")
    return file_url_pairs

def redownload_bad_files(bad_file_url_pairs):
    for elem in bad_file_url_pairs:
        bad_file_path = elem[0]
        url = elem[1]
        get_html_from_page(url,bad_file_path,False,True)


def get_rids3(num_records, num_pages):
    temp_num_records = num_records
    rid_list = []
    i = 0
    page_num = 0
    if (num_records < 10):
        small_record_num = 0
        while small_record_num < num_records:
            rid_list.append("0" + "x" + str(small_record_num))
            small_record_num += 1
        return rid_list
    else:
        while page_num < num_pages:
            while i < 10:
                if page_num == 0:
                    rid_list.append('0' + "x" + str(i))
                else:
                    rid_list.append(str(page_num) + '0' + "x" + str(i))
                i += 1
            i = 0
            page_num += 1
    return rid_list


def get_rids2(num_records, num_pages):
    temp_num_records = num_records
    rid_list = []
    i = 0
    page_num = 0

    if (int(num_records) < 10):
        small_record_num = 0
        while small_record_num < int(num_records):
            rid_list.append("0" + "x" + str(small_record_num))
            small_record_num += 1
        return rid_list
    else:
        num_record_count = 0
        while page_num < num_pages and num_record_count < int(num_records):
            while i < 10:
                if page_num == 0:
                    rid_list.append('0' + "x" + str(i))
                else:
                    if (int(str(page_num) + str(i)) < int(num_records)):
                        rid_list.append(str(page_num) + '0' + "x" + str(i))
                num_record_count += 1
                i += 1
            i = 0
            page_num += 1
    return rid_list


def get_all_rids2(num_records_list, num_pages_list):
    all_rids_list = []
    for num_records, num_pages in zip(num_records_list, num_pages_list):
        all_rids_list.append(get_rids2(num_records, num_pages))
    return all_rids_list


def get_rids(num_pages):
    rid_list = []
    i = 0
    page_num = 0
    if (num_pages < 10):
        small_page_num = 0
        while small_page_num < num_pages:
            rid_list.append(str(page_num) + "x" + str(i))
            small_page_num += 1
        return rid_list

    while page_num < num_pages:
        while i < 10:
            rid_list.append(str(page_num) + "x" + str(i))
            i += 1
        i = 0
        page_num += 1
    return rid_list


def google_captcha_detected(soup):
    parent_results = soup.findAll('div', class_="g-recaptcha")
    if (len(parent_results) > 0):
        return True
    else:
        return False


def gen_all_urls(names_and_locs):
    url_list = []
    for elem in names_and_locs:
        url = gen_url(elem[0], elem[1], elem[2], elem[3])
        url_list.append(url)
    return url_list


def gen_param_list_for_urls(names_and_locs):
    gen_list = []
    for idx, val in enumerate(names_and_locs):
        first_name = names_and_locs[idx][0].split()[0]
        last_name = names_and_locs[idx][0].split()[1]
        middle_name = ''
        if(len(names_and_locs[idx][0].split()) >= 3):
            first_name = names_and_locs[idx][0].split()[0]
            middle_name = names_and_locs[idx][0].split()[1]
            last_name = names_and_locs[idx][0].split()[2]
        title = ''
        if (len(names_and_locs[idx][0].split()) >= 4):
            print(names_and_locs[idx][0].split())
            first_name = names_and_locs[idx][0].split()[0]
            middle_name = names_and_locs[idx][0].split()[1]
            last_name = names_and_locs[idx][0].split()[2]
            title = names_and_locs[idx][0].split()[3]
        print("loc")
        print(names_and_locs[idx][1])
        city = names_and_locs[idx][1].split(',')[0]
        print(city)
        #city = city.replace(',', '')

        state = names_and_locs[idx][1].split(',')[1]
        elem_to_add = [first_name, last_name, city, state,middle_name,title]
        gen_list.append(elem_to_add)
    return gen_list[0]


def get_file_num(file_path):
    last_file_name = basename(file_path)
    last_file_name = last_file_name[4:]
    last_file_name = last_file_name.split('.', 1)[0]
    file_num = int(last_file_name)
    return file_num


def get_latest_file_number(file_list):
    num_list = []
    for elem in file_list:
        num_list.append((get_file_num(elem)))
    return max(num_list)


def get_latest_file_path(file_list):
    latest_num = get_latest_file_path(file_list)
    for elem in file_list:
        temp_num = get_latest_file_number(elem)
        if temp_num == latest_num:
            return elem


def get_html_from_page(video_url, path_to_write_to, write_to_file=True, full_path=False):
    global GLOBAL_COUNTER
    GLOBAL_COUNTER += 1
    g_c_interval = random.randrange(45, 55)
    if (GLOBAL_COUNTER >= g_c_interval):
        print("Begin waiting")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        interval = random.randrange(5, 9)
        print("Waiting " + str(interval) + " minutes.")
        time.sleep(60 * interval)
        GLOBAL_COUNTER = 0


    # user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    # user_agent = 'your bot 0.2222'
    # headers = {'User-Agent': user_agent, }

    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """
    # proxy_ip = FreeProxy().get()

    # proxy = urllib2.ProxyHandler({"http": proxy_ip})
    # opener = urllib2.build_opener(proxy)
    # opener.addheaders = [('User-Agent',user_agent)]
    # urllib2.install_opener(opener)

    # req = urllib.request.Request(video_url)
    # req.add_header('User-Agent', user_agent)
    # page = urllib.request.urlopen(req)

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random}
    time.sleep(random.randrange(11, 13))  # to prevent captcha

    result = requests.get(video_url, headers=headers)

    # "http://webcache.googleusercontent.com/search?q=cache:"
    # pp.pprint(page.info())
    # request = urllib.request.Request(video_url, None, headers)  # The assembled request
    # response = urllib.request.urlopen(request)

    data = result.text  # The data u need
    cloud_soup = BeautifulSoup(data, 'html.parser')
    def remove_line_break_and_concat(html_elem):
        html_elem = str.split(html_elem.get_text())
        parsed_text_full = ""
        if "<br>" in html_elem:
            html_elem.remove(html_elem.index("<br>"))
        for elem in html_elem:
            parsed_text_full += elem + " "
        parsed_text_full = parsed_text_full.strip()
        return parsed_text_full
    def get_address(soup):
        if soup is not None:
            address_html = soup.find('a', class_="link-to-more olnk")
            if address_html is not None:
                address_html = remove_line_break_and_concat(address_html)
                return address_html
            else:
                return ''
        else:
            return ''

    address = get_address(cloud_soup)
    if address != '':
        if " CO " not in address:
            print("Address" + address)
            print("URL:" + video_url)
            print("Address doesn't match filter. Discarding...")
            f = open("/Users/howie/PycharmProjects/webscraper/venv/filtered_out_by_address.txt", "a")
            f.write(video_url)
            f.close()


            return None,None



    if (google_captcha_detected(cloud_soup)):
        print("Google Captcha detected.")
        if (write_to_file is True):
            f = open("/Users/howie/PycharmProjects/webscraper/venv/google_captcha_file.txt", "a")
            f.write(video_url)
            f.close()

        return cloud_soup,None
    if cloud_fare_denial_detected(cloud_soup):
        print("Cloud fare protection detected! Aborting before writing bad value to file.")
        print("Guilty URL: " + video_url)
        if (write_to_file is True):
            f = open("/Users/howie/PycharmProjects/webscraper/venv/cloud_fare_file.txt", "w")
            f.write(video_url)
            f.close()

        system('say "Aborting due to cloudfare denial"')
        input("Press Enter to Exit")

        sys.exit()
    if detect_no_results_found(cloud_soup):
        if write_to_file is True:
            f = open("/Users/howie/PycharmProjects/webscraper/venv/no_content_urls.txt", "a")
            f.write(video_url + "\n")
            f.close()

        print("No results for this file found. Skipping...")
        return None,None
    print("Still safe.")
    mypath = path_to_write_to
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    detail_file_path = ''
    file_path = ""
    if (len(onlyfiles) == 0):
        file_path = join(mypath, "html0.html")
        if full_path is True:
            file_path = full_path
        # print(str(file_path))
        f = open(file_path, "w")
        f.write(data)
        f.close()


    else:
        file_num = get_latest_file_number(onlyfiles)
        file_path_num = file_num + 1
        file_path_name = "html" + str(file_path_num) + ".html"
        file_path = join(mypath, file_path_name)
        if (file_path in onlyfiles):
            if (stat(file_path).st_size != 0):
                print("got here???!!!???")
                file_path_num = file_num + 2
                file_path_name = "html" + str(file_path_num) + ".html"
                file_path = join(mypath, file_path_name)

        else:
            if full_path:
                file_path = full_path
            f = open(file_path, "w")
            f.write(data)
            f.close()

    detail_file_path = file_path
    if (write_to_file is True):
        f = open("/Users/howie/PycharmProjects/webscraper/venv/files_and_urls.txt", "a")
        f.write(basename(file_path) + ";" + video_url + "\n")
        f.close()

    # pp.pprint(data)
    # soup = BeautifulSoup(open(file_path),"html.parser")
    # soup = BeautifulSoup(data, 'html.parser')

    return cloud_soup,detail_file_path
    # print(data)
    # page = urllib.request.urlopen(video_url)
    # soup = BeautifulSoup(page, 'html.parser')
    # print(soup)

    # f = open("html_sample.txt", "w")
    # f.write(soup.prettify())
    # f.close()
    # print(soup.prettify())


def parse_html2(soup, name_searched='', loc_searched='', url='', file='', reproduce_url=False):
    global GLOBAL_P_COUNTER
    pp = pprint.PrettyPrinter(indent=4)

    parent_results = soup.findAll('div', class_="col-12 col-sm-11")

    # accepts html
    def remove_line_break_and_concat(html_elem):
        html_elem = str.split(html_elem.get_text())
        parsed_text_full = ""
        if "<br>" in html_elem:
            html_elem.remove(html_elem.index("<br>"))
        for elem in html_elem:
            parsed_text_full += elem + " "
        parsed_text_full = parsed_text_full.strip()
        return parsed_text_full

    def get_name_age_and_year(original_soup):
        results = original_soup.find('div', class_="row pl-md-2")
        if results is not None:
            name = results.find('span', class_="h2")
            name = remove_line_break_and_concat(name)
            results = remove_line_break_and_concat(results.find('span', class_="content-value"))
            if results is not None:
                age_and_year = results.split()
            if (len(age_and_year) > 0):
                age = age_and_year[1]
            else:
                age = ['', '']
            if (len(age_and_year) > 3):
                year = age_and_year[2] + " " + age_and_year[3]
                year = year.replace("(", "")
                year = year.replace(")", "")
            else:
                year = ''

        else:
            name = ''
            age = ''
            year = ''

        return name, age, year

    def get_address(soup):
        if soup is not None and len(soup) > 0:
            address_html = soup[0].find('a', class_="link-to-more olnk")
            if address_html is not None:
                address_html = remove_line_break_and_concat(address_html)
                return address_html
            else:
                return ''
        else:
            return ''

    def parse_bus(bus):
        l = []
        text_bus = bus.get_text()
        # pp.pprint("text bus")
        # pp.pprint(text_bus)
        # pp.pprint("</text bus>")
        # pp.pprint(bus.get_text())
        text_bus_trimmed = bus.get_text().split("\n")
        trimmed_l = []
        if text_bus_trimmed is not None:
            for idx, elem in enumerate(text_bus_trimmed):
                if elem.strip() != '':
                    trimmed_l.append(elem.strip())
                    # pp.pprint("text bus trimmed")
                    # pp.pprint(text_bus_trimmed[idx])
        for elem in trimmed_l:
            l.append(elem)
        # l_to_add = text_bus_trimmed
        # pp.pprint(l)
        # pp.pprint("LLL")
        # pp.pprint(l)
        # pp.pprint("LLLLL")
        return l

    def parse_vals_true(sub_soup, is_bus=False, get_dates=False):
        unparsed_emails_true = sub_soup.findAll('div', class_="content-value")
        # pp.pprint(unparsed_emails_true)
        email_list_parsed = []
        date_list = []

        for elem in unparsed_emails_true:
            if not is_bus:
                date = ''
                if elem is not None:
                    date = elem.find('span', class_="content-label smaller")
                    if date is not None:
                        date_list.append(date.getText().strip())
                    else:
                        date_list.append(' ')
                # pp.pprint("email list parsed")
                email_list_parsed.append(remove_line_break_and_concat(elem))
                # pp.pprint(email_list_parsed)
            else:
                if elem is not None:
                    date = elem.find('span', class_="content-label smaller")
                    if date is not None:
                        date_list.append(date)
                    else:
                        date_list.append(' ')
                    l_to_add = parse_bus(elem)
                    # pp.pprint("L to add")
                    # pp.pprint(l_to_add)
                    email_list_parsed.append(l_to_add)
                    # email_list_parsed.append(l_to_add)
        if get_dates == True:
            # pp.pprint("DATE LIST")
            # pp.pprint(date_list)
            # pp.pprint("END DATE LIST")
            return email_list_parsed, date_list
        else:
            return email_list_parsed

    def get_index_of_elem(parent_soup, needle):
        for idx, elem in enumerate(parent_soup):
            unparsed_emails_true = elem.find('div', class_="content-label h5")
            # pp.pprint(parent_soup[4].getText())
            # pp.pprint(unparsed_emails_true.getText())
            if (needle in unparsed_emails_true.getText()):
                return idx

        return -1

    name, age, year = get_name_age_and_year(soup)
    """
    if parent_results is not None:
        idx = get_index_of_elem(parent_results,"Email Addresses")
        if idx is not -1:
            parsed_emails_true = parse_vals_true(parent_results[idx])
        else:
            parsed_emails_true = []
    else:
        print("PARENT RESULTS NONE")
        parsed_emails_true = []
    if parent_results is not None:
        idx = get_index_of_elem(parent_results,"Previous Addresses")
        if idx is not -1:
            parsed_addresses_true,parsed_address_dates_true = parse_vals_true(parent_results[idx],False,True)
        else:
            parsed_addresses_true = []
            parsed_address_dates_true = []
    else:
        parsed_addresses_true = []
        parsed_address_dates_true = []

    if parent_results is not None:
        idx = get_index_of_elem(parent_results,"Possible Businesses")
        if idx is not -1:
            parsed_buses_true, parsed_bus_dates_true = parse_vals_true(parent_results[idx],True,True)
        else:
            parsed_buses_true = []
            parsed_bus_dates_true = []
    else:
        parsed_buses_true = []
        parsed_bus_dates_true = []

    if parent_results is not None:
        idx = get_index_of_elem(parent_results,"Phone Numbers")
        if idx is not -1:
            parsed_numbers =  parse_vals_true(parent_results[idx],False,False)
        else:
            parsed_numbers = []
    else:
        parsed_numbers = []

    curr_address = get_address(parent_results)





    if name_searched == '':
        if(name == ''):
            name,age,year = get_name_age_and_year(soup)
        print("name")
        print(name)
        if name != '':
            name_searched2 = name.split()
            if(len(name_searched2) > 2):
                name_searched = name_searched2[0] + " " + name_searched2[2]
            elif(len(name_searched2) == 2):
                name_searched = name_searched2[0] + " " + name_searched2[1]
            else:
                name_searched = ''
        else:
            name_searched = ''
    if loc_searched == '' and name_searched != '':
        names_and_locs = get_names_and_locations("RA_List.xlsx")
        for elem in names_and_locs:
            name2 = elem[0]
            if name_searched in name2:
                loc_searched = elem[1]

    if parsed_buses_true is not None and len(parsed_buses_true) > 0:
        default_business = ''.join(parsed_buses_true[0])
    else:
        default_business = ''

    """

    # p = Person(default_business,name_searched,loc_searched,url,name,age,year,curr_address,parsed_numbers,parsed_emails_true,parsed_addresses_true,parsed_buses_true,parsed_bus_dates_true,parsed_address_dates_true,file)
    # print(str(p))
    GLOBAL_P_COUNTER += 1
    print("GLOBAL P COUNTER")
    print(GLOBAL_P_COUNTER)
    return p


def parse_html(soup, name_searched='', loc_searched='', url='', file='', reproduce_url=False):
    pp = pprint.PrettyPrinter(indent=4)

    parent_results = soup.findAll('div', class_="col-12 col-sm-11")

    def remove_line_break_and_concat(html_elem):
        html_elem = str.split(html_elem.get_text())
        parsed_text_full = ""
        if "<br>" in html_elem:
            html_elem.remove(html_elem.index("<br>"))
        for elem in html_elem:
            parsed_text_full += elem + " "
        parsed_text_full = parsed_text_full.strip()
        return parsed_text_full

    def get_name_age_and_year(original_soup):
        results = original_soup.find('div', class_="row pl-md-2")
        if results is not None:
            name = results.find('span', class_="h2")
            name = remove_line_break_and_concat(name)
            results = remove_line_break_and_concat(results.find('span', class_="content-value"))
            if results is not None:
                age_and_year = results.split()
            if (len(age_and_year) > 0):
                age = age_and_year[1]
            else:
                age = ['', '']
            if (len(age_and_year) > 3):
                year = age_and_year[2] + " " + age_and_year[3]
                year = year.replace("(", "")
                year = year.replace(")", "")
            else:
                year = ''

        else:
            name = ''
            age = ''
            year = ''

        return name, age, year

    def get_address(soup):
        if soup is not None and len(soup) > 0:
            address_html = soup[0].find('a', class_="link-to-more olnk")
            if address_html is not None:
                address_html = remove_line_break_and_concat(address_html)
                return address_html
            else:
                return ''
        else:
            return ''

    def parse_bus(bus):
        l = []
        text_bus = bus.get_text()
        # pp.pprint("text bus")
        # pp.pprint(text_bus)
        # pp.pprint("</text bus>")
        # pp.pprint(bus.get_text())
        text_bus_trimmed = bus.get_text().split("\n")
        trimmed_l = []
        if text_bus_trimmed is not None:
            for idx, elem in enumerate(text_bus_trimmed):
                if elem.strip() != '':
                    trimmed_l.append(elem.strip())
                    # pp.pprint("text bus trimmed")
                    # pp.pprint(text_bus_trimmed[idx])
        for elem in trimmed_l:
            l.append(elem)
        # l_to_add = text_bus_trimmed
        # pp.pprint(l)
        # pp.pprint("LLL")
        # pp.pprint(l)
        # pp.pprint("LLLLL")
        return l

    def parse_vals_true(sub_soup, is_bus=False, get_dates=False):
        unparsed_emails_true = sub_soup.findAll('div', class_="content-value")
        # pp.pprint(unparsed_emails_true)
        email_list_parsed = []
        date_list = []

        for elem in unparsed_emails_true:
            if not is_bus:
                date = ''
                if elem is not None:
                    date = elem.find('span', class_="content-label smaller")
                    if date is not None:
                        date_list.append(date.getText().strip())
                    else:
                        date_list.append(' ')
                # pp.pprint("email list parsed")
                email_list_parsed.append(remove_line_break_and_concat(elem))
                # pp.pprint(email_list_parsed)
            else:
                if elem is not None:
                    date = elem.find('span', class_="content-label smaller")
                    if date is not None:
                        date_list.append(date)
                    else:
                        date_list.append(' ')
                    l_to_add = parse_bus(elem)
                    # pp.pprint("L to add")
                    # pp.pprint(l_to_add)
                    email_list_parsed.append(l_to_add)
                    # email_list_parsed.append(l_to_add)
        if get_dates == True:
            # pp.pprint("DATE LIST")
            # pp.pprint(date_list)
            # pp.pprint("END DATE LIST")
            return email_list_parsed, date_list
        else:
            return email_list_parsed

    def get_index_of_elem(parent_soup, needle):
        for idx, elem in enumerate(parent_soup):
            unparsed_emails_true = elem.find('div', class_="content-label h5")
            # pp.pprint(parent_soup[4].getText())
            # pp.pprint(unparsed_emails_true.getText())
            if (needle in unparsed_emails_true.getText()):
                return idx

        return -1

    name, age, year = get_name_age_and_year(soup)
    if parent_results is not None:
        idx = get_index_of_elem(parent_results, "Email Addresses")
        if idx is not -1:
            parsed_emails_true = parse_vals_true(parent_results[idx])
        else:
            parsed_emails_true = []
    else:
        print("PARENT RESULTS NONE")
        parsed_emails_true = []
    # pp.pprint(parsed_emails_true)
    if parent_results is not None:
        idx = get_index_of_elem(parent_results, "Previous Addresses")
        if idx is not -1:
            parsed_addresses_true, parsed_address_dates_true = parse_vals_true(parent_results[idx], False, True)
        else:
            parsed_addresses_true = []
            parsed_address_dates_true = []
    else:
        parsed_addresses_true = []
        parsed_address_dates_true = []

    # pp.pprint(parsed_addresses_true)
    if parent_results is not None:
        idx = get_index_of_elem(parent_results, "Possible Businesses")
        if idx is not -1:
            parsed_buses_true, parsed_bus_dates_true = parse_vals_true(parent_results[idx], True, True)
        else:
            parsed_buses_true = []
            parsed_bus_dates_true = []
    else:
        parsed_buses_true = []
        parsed_bus_dates_true = []

    if parent_results is not None:
        idx = get_index_of_elem(parent_results, "Phone Numbers")
        if idx is not -1:
            parsed_numbers = parse_vals_true(parent_results[idx], False, False)
        else:
            parsed_numbers = []
    else:
        parsed_numbers = []

    curr_address = get_address(parent_results)

    if name_searched == '':
        if (name == ''):
            name, age, year = get_name_age_and_year(soup)
        print("name")
        print(name)
        if name != '':
            name_searched2 = name.split()
            if (len(name_searched2) > 2):
                name_searched = name_searched2[0] + " " + name_searched2[2]
            elif (len(name_searched2) == 2):
                name_searched = name_searched2[0] + " " + name_searched2[1]
            else:
                name_searched = ''
        else:
            name_searched = ''
    if loc_searched == '' and name_searched != '':
        names_and_locs = get_names_and_locations("RA_List.xlsx")
        for elem in names_and_locs:
            name2 = elem[0]
            if name_searched in name2:
                loc_searched = elem[1]

    if parsed_buses_true is not None and len(parsed_buses_true) > 0:
        default_business = ''.join(parsed_buses_true[0])
    else:
        default_business = ''

    p = Person(default_business, name_searched, loc_searched, url, name, age, year, curr_address, parsed_numbers
               , parsed_emails_true, parsed_addresses_true, parsed_buses_true, parsed_bus_dates_true,
               parsed_address_dates_true, file)
    print(str(p))
    # print("Person")
    # pp.pprint(str(p))
    return p
    # for elem in xz:
    #   for y in elem:
    #      print(y)
    #  print("hhhhhhhhhhhhhhhhhhhhhddhdhdhdhdhdhdhdhdhdhdhdhdhdhd")


def main():
    pass


def get_all_html_for_one_searched_person(urls):
    url_list = []
    for elem in name:
        url = gen_url(elem[0], elem[1], elem[2], elem[3], get_all_rids(25))
        url_list.append(url)
    return url_list


def get_all_html(urls, path_to_write_to, write_to_file):
    global GLOBAL_NO_CONTENT_COUNTER
    html_list = []
    file_path_list = []
    for elem in urls:
        soup,file_path = get_html_from_page(elem, path_to_write_to, write_to_file)
        if soup is None:
            print("Soup was none. Skipping...")
            continue
        captcha_detected = google_captcha_detected(soup)
        if (captcha_detected is False):
            if soup not in html_list:
                html_list.append(soup)

            print("Got html from: " + str(elem))
        else:
            system('say "Google captcha detected"')
            input("Google reCaptcha detected. Please navigate to current URL and solve captcha. Press Enter when "
                  "finished.")
            i = 0
            while (i < 3 and captcha_detected == True):
                soup2,file_path = get_html_from_page(elem, path_to_write_to, write_to_file)
                if soup2 is None:
                    break
                captcha_detected = google_captcha_detected(soup2)
                if (captcha_detected is False):
                    if soup2 not in html_list:
                        html_list.append(soup2)
                    print("Got html from: " + str(elem))
                    i = 4
                    break
                i += 1
        if file_path is not None:
            file_path_list.append((file_path,elem))

    print("Scraped all html.")
    # dill.dump(html_list,f)
    return html_list,file_path_list

def grab_all_bad_file_paths():
    mypath = "/Users/howie/PycharmProjects/webscraper/venv/html_folder"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    htmls = []
    bad_htmls_and_urls = []

    for idx, elem in enumerate(onlyfiles):
        full_path = join(mypath, elem)
        html = BeautifulSoup(open(full_path), "html.parser")
        if detect_no_results_found(html) is True or google_captcha_detected(html) is True or cloud_fare_denial_detected(html) is True:
            htmls.append(html)
        else:
            continue
            # print("bad file")
            #print(full_path)
            # print("end bad file")
            # htmls.append(idx - 1)
            # print("Guilty file: " + full_path)
            # file_num = get_file_num(full_path)
            # url = get_supposed_url_from_file_num(file_num)
            # bad_htmls_and_urls.append((full_path,url))
    """
    with open('bad_files.txt', 'w') as f:
        for item in bad_htmls_and_urls:
            path = item[0]
            url = item[1]
            f.write(path + ", " + "\n")
            f.close()
    """

    print("len htmls")

    print(len(htmls))
    html2 = reversed(htmls)
    return list(html2)

    pass

def grab_all_html_from_files():
    mypath = "/Users/howie/PycharmProjects/webscraper/venv/html_folder"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    htmls = []
    bad_htmls_and_urls = []

    for idx, elem in enumerate(onlyfiles):
        full_path = join(mypath, elem)
        html = BeautifulSoup(open(full_path), "html.parser")
        if detect_no_results_found(html) is False and google_captcha_detected(html) is False:
            htmls.append(html)
        else:

            # print("bad file")
            print(full_path)
            # print("end bad file")
            # htmls.append(idx - 1)
            # print("Guilty file: " + full_path)
            # file_num = get_file_num(full_path)
            # url = get_supposed_url_from_file_num(file_num)
            # bad_htmls_and_urls.append((full_path,url))
    """
    with open('bad_files.txt', 'w') as f:
        for item in bad_htmls_and_urls:
            path = item[0]
            url = item[1]
            f.write(path + ", " + "\n")
            f.close()
    """

    print("len htmls")

    print(len(htmls))
    html2 = reversed(htmls)
    return list(html2)


def detect_no_results_found(soup):
    text = soup.getText()
    if "We could not find any records for that search criteria" in text:
        return True
    else:
        return False


def parse_all_html3(names_and_locs, htmls, url_list, file_list):
    pp = pprint.PrettyPrinter(indent=4)

    person_list = []
    # pp.pprint("htmls::::::::")
    # pp.pprint(htmls)
    f = open('/Users/howie/PycharmProjects/webscraper/venv/persons3.p', 'ab')
    print("len url list")
    print(len(url_list))
    print(len(list(htmls)))
    for html in htmls:
        if (html != '\n' and html != "html" and not isinstance(html, int)):
            print("got here instead")
            person = parse_html(html)
            # print("person:::::")
        else:
            person = Person('ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff')
        # pickle.dump(person, f)
        person_list.append(person)

        # print("Parsed:" + " " + str(person.bus) + "," + str(person.name_searched) + ", " + str(person.loc_searched) + str(person.tps_name))
    f.close()
    print("LEN PERSONS")
    print(len(person_list))
    return person_list


def parse_all_html2(names_and_locs, htmls, url_list, file_list):
    print("CAN I")
    pp = pprint.PrettyPrinter(indent=4)

    person_list = []
    # pp.pprint("htmls::::::::")
    # pp.pprint(htmls)

    url_list = []
    for x in range(181):
        url_list.append("")
    file_list = []
    for x in range(181):
        file_list.append("")
    print("LENLEN")
    print(len(list(htmls)))
    print(len(names_and_locs))
    print(len(url_list))
    print(len(file_list))
    print("END LEN LEN")
    for elem in list(htmls):
        html = elem[0]
        # print("html")
        # pp.pprint(html)
        # print("close html")
        url = elem[1]
        file = elem[2]
        if True:
            person = parse_html(html, '', '', url, file)
            print("got here!!!!!!")
            # print("person:::::")
        else:
            print("got here???????")
            person = Person('ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff', 'ff')
        # pickle.dump(person, f)
        person_list.append(person)

        # print("Parsed:" + " " + str(person.bus) + "," + str(person.name_searched) + ", " + str(person.loc_searched) + str(person.tps_name))
    # f.close()
    print("LEN PERSONS")
    print(len(person_list))
    return person_list





def write_to_excel_file(persons, workbook):
    worksheet = workbook.add_worksheet()
    row = 1
    col = 0
    header_row = 0
    worksheet.write(header_row, col, "Business")
    worksheet.write(header_row, col + 1, "Name")
    worksheet.write(header_row, col + 2, "Location")
    worksheet.write(header_row, col + 3, "Truepeopleurl")
    worksheet.write(header_row, col + 4, "TPS Name")
    worksheet.write(header_row, col + 5, "TPS Age")
    worksheet.write(header_row, col + 6, "TPS Birth Month and Year")
    worksheet.write(header_row, col + 7, "TPS Current Address")

    i = 0
    while i < 100:
        worksheet.write(header_row, col + 8 + i, "TPS Phone Number" + " " + str(i + 1))
        i += 1
    col = 8 + i
    j = 0
    while j < 100:
        worksheet.write(header_row, col + j, "TPS Email Address" + " " + str(j + 1))
        j += 1
    col += j

    j = 0
    temp_col = col + 1
    num_index = 1
    while j < 200:
        worksheet.write(header_row, col + j, "Previous Address" + " " + str(num_index))
        j += 1
        worksheet.write(header_row, col + j, "Previous Address" + " " + str(num_index) + " Date")
        j += 1
        num_index += 1
    col += j

    j = 0
    num_index = 1
    # col1 = col
    # col2 = col
    while j < 300:
        worksheet.write(header_row, col + j, "Possible_Business_" + str(num_index))
        j += 1
        worksheet.write(header_row, col + j, "Possible_Business_Address_" + str(num_index))
        j += 1
        worksheet.write(header_row, col + j, "Possible_Business_Address_" + str(num_index) + " Date")
        j += 1
        num_index += 1

    # worksheet.write(header_row,col+9,"TPS Age")
    # worksheet.write(header_row,col+10,"TPS Age")
    row = 1
    col = 0
    for person in persons.person_list:
        worksheet.write(row, col, person.bus)
        worksheet.write(row, col + 1, person.name_searched)
        worksheet.write(row, col + 2, person.loc_searched)
        worksheet.write(row, col + 3, person.details_url)
        worksheet.write(row, col + 4, person.tps_name)
        worksheet.write(row, col + 5, person.tps_age)
        worksheet.write(row, col + 6, person.birth_date)
        worksheet.write(row, col + 7, person.curr_address)
        col = col + 8
        i = 0
        for idx, elem in enumerate(person.phone_nums):
            worksheet.write(row, col + i, elem)
            i += 1
        col = 108
        i = 0
        for idx, elem in enumerate(person.email_addresses):
            worksheet.write(row, col + idx, elem)
            i = idx
        col = 208
        i = 0
        for idx, elem in enumerate(person.prev_addresses):
            worksheet.write(row, col + i, elem.split('(')[0])
            i += 1
            # print("prev address_Dates to write")
            # pp.pprint(person.prev_address_dates[idx])
            # print("end prev aaddress dates to write")
            worksheet.write(row, col + i, person.prev_address_dates[idx])
            i += 1

        col = 408
        i = 0
        for idx, elem in enumerate(person.possible_buses_and_addresses):
            # print("elem")
            # pp.pprint(elem)
            # print("</elem>")
            worksheet.write(row, col + i, elem[0])
            i += 1
            if (len(elem) >= 2):
                worksheet.write(row, col + i, elem[1])
            i += 1
            # pp.pprint("DATES")
            # pp.pprint(person.bus_dates)
            # pp.pprint("ENDDATES")
            worksheet.write(row, col + i, person.bus_dates[idx])  # person.bus_dates[idx])
            i += 1

        col = 708
        i = 0
        row += 1
        col = 0
    workbook.close()


def csv_from_excel(workbook_path, csv_output_file_path):
    wb = xlrd.open_workbook(workbook_path)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(csv_output_file_path, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


def pair_names_locs_and_rid_list(names_and_locs, rid_lists):
    pair_list = []
    for rid_list, name_and_loc in zip(rid_lists, names_and_locs):
        if [name_and_loc, rid_list] not in pair_list:
            pair_list.append([name_and_loc, rid_list])
    return pair_list


def gen_all_urls_for_all_pages(names_and_locs, rid_lists):
    pp = pprint.PrettyPrinter(indent=4)
    url_list = []
    pair_list = pair_names_locs_and_rid_list(names_and_locs, rid_lists)
    # pp.pprint(pair_list)
    for pair in pair_list:
        elem = pair[0]
        # print('elem')
        # pp.pprint(elem)
        rid_list = pair[1]
        for rid in rid_list:

            url = gen_url(elem[0], elem[1], elem[2], elem[3], rid)
            if elem not in url_list:
                url_list.append(url)
    """
    for elem in names_and_locs:
        url = ''
        url = gen_url(elem[0], elem[1], elem[2], elem[3],rid)
        url_list.append(url)
    return url_list
    """
    return url_list




def actual_main():
    pp = pprint.PrettyPrinter(indent=4)
    names_and_locs = get_names_and_locations("RA_List.xlsx")
    # pp.pprint(names_and_locs)
    param_list = gen_param_list_for_urls(names_and_locs)
    # pp.pprint(param_list)
    urls = gen_all_urls(param_list)
    htmls = get_all_html(urls)
    # htmls = BeautifulSoup(open("html_sample.html"), "html.parser")
    persons = parse_all_html2(htmls)

    # person = parse_html(htmls)
    # persons = []
    # persons.append(person)

    workbook = xlsxwriter.Workbook('scraped_data.xlsx')
    print("Writing to files...")
    write_to_excel_file(persons, workbook)

    csv_from_excel('scraped_data.xlsx', 'scraped_data.csv')
    # remove("scraped_data.xlsx")
    print("Finished.")

    # os.remove("scraped_data.xlsx") --Enable at end.

    # for elem in persons:
    #   pp.pprint(str(elem))
    # with open('your_file.txt', 'w') as f:
    #   for item in persons:
    #      f.write("%s\n" % str(item))
    # pp.pprint(x)

    # f = open("demofile2.txt", "a")
    # f.write("Now the file has more content!")
    # f.close()
    # get_html_from_page("")
    # parse_html("")


def get_all_num_records(htmls_with_nums):
    num_record_list = []
    for elem in htmls_with_nums:
        num_record_list.append(get_num_results(elem))
    return num_record_list


def group_all_urls_by_person(name_and_loc_list, url_list):
    grouped_urls = []
    for elem in name_and_loc_list:
        first_name = elem[0]
        last_name = elem[1]
        city = elem[2]
        state = elem[3]
        this_person_url_list = []
        for url in url_list:
            if first_name in url and last_name in url and city in url and state in url:
                this_person_url_list.append(url)
        grouped_urls.append(this_person_url_list)
    return grouped_urls


def group_all_files_by_person(name_and_loc_list, file_list):
    grouped_urls = []
    for elem in name_and_loc_list:
        first_name = elem[0]
        last_name = elem[1]
        city = elem[2]
        state = elem[3]
        this_person_url_list = []
        person_list = parse_all_html2(file_list)
        for person in person_list:
            if first_name in person.first_name and last_name in person.last_name and city in person.city and state in person.state:
                this_person_url_list.append(person.details_url)
        grouped_urls.append(this_person_url_list)

    return grouped_urls


def reproduce_all_urls_from_files(files):
    url_and_file_list = []
    person_list = parse_all_html2(file_list)

    parse_only_url_fields_from_file()
    return url_and_file_list


def flatten_list(l):
    flat_list = []
    for sublist in l:
        for item in sublist:
            flat_list.append(item)
    return flat_list


def cloud_fare_denial_detected(soup):
    cloud_fare_title = soup.find('title')
    if cloud_fare_title.getText is not None and len(cloud_fare_title) > 0:
        if ("Access denied | www.truepeoplesearch.com used Cloudflare to restrict access" in cloud_fare_title):
            return True
        else:
            return False
    return False




def sort_files_by_ascending(og_list):
    nums_at_start = []
    num_and_file_list = []
    for elem in og_list:
        file_num = get_file_num(elem)
        num_and_file_list.append((file_num, elem))
        # num_and_file_list.append(file_num)
        temp_elem = str(get_file_num(elem)) + elem
        nums_at_start.append(temp_elem)
        # print(temp_elem)
    num_and_file_list.sort(key=lambda x: x[0])
    pp.pprint(num_and_file_list)
    y = []
    for elem in num_and_file_list:
        y.append(elem[1])
    return y


def sort_files_shift_nums_and_delete_cloud_fare(file_path_list):
    pp = pprint.PrettyPrinter(indent=4)
    mypath = "html_folder"

    def detect_in_all_cloudfare(file_path_list, mypath):
        bad_list = []
        for elem in file_path_list:
            soup = BeautifulSoup(open(join(mypath, elem)), "html.parser")
            cloud_fare = cloud_fare_denial_detected(soup)
            if cloud_fare:
                bad_list.append(join(mypath, elem))
        return bad_list

    def delete_items_from_og_list(og_list, bad_list):
        # good_list = []
        for elem in bad_list:
            if elem in og_list:
                og_list.remove(elem)
        return og_list

    def delete_bad_files_from_directory(bad_list):
        for elem in bad_list:
            if exists(elem):
                remove(elem)
            else:
                print("The file does not exist")

    def sort_remaining_files_by_ascending2(og_list):
        nums_at_start = []
        num_and_file_list = []
        for elem in og_list:
            file_num = get_file_num(elem)
            num_and_file_list.append((file_num, elem))
            # num_and_file_list.append(file_num)
            temp_elem = str(get_file_num(elem)) + elem
            nums_at_start.append(temp_elem)
            # print(temp_elem)
        num_and_file_list.sort(key=lambda x: x[0])
        pp.pprint(num_and_file_list)
        y = []
        for elem in num_and_file_list:
            y.append(elem[1])
        return y

    def sort_remaining_files_by_ascending(og_list):
        sorted_list = []
        num_list = []
        num_and_file_list = []
        for elem in og_list:
            file_num = get_file_num(elem)
            num_and_file_list.append((file_num, elem))
            num_list.append(file_num)

        pp.pprint(num_and_file_list)
        num_list.sort()
        print("fjdfjfjfjf")
        pp.pprint(num_list)
        print("jfjfjfjfjf")
        sorted_list = num_list

        for elem in num_list:
            for item in og_list:
                str_elem = str(elem)
                if str_elem in item:
                    print(elem)
                    # print(item)
                    if item not in sorted_list and str_elem.isnumeric():
                        sorted_list[elem] = item
        return sorted_list

    def reassign_numbers(dir_path, file_path_list):

        reassigned_list = []
        for idx, elem in enumerate(file_path_list):
            base_name = basename(elem)
            dir_name = dir_path
            base_name = "html" + str(idx) + ".html"
            # new_dir_path = join(dir_name)
            reassigned_list.append(join(dir_name, base_name))
        file_path_list2 = []
        for elem in file_path_list:
            file_path_list2.append(join(dir_path, elem))
        assigned_list = list(zip(file_path_list2, reassigned_list))
        for elem in assigned_list:
            rename(elem[0], elem[1])
        pp.pprint(assigned_list)
        return reassigned_list

    # bad_list = detect_in_all_cloudfare(file_path_list,mypath)
    # pp.pprint(bad_list)
    # delete_bad_files_from_directory(bad_list)
    # pp.pprint(bad_list)
    sorted_list = sort_remaining_files_by_ascending2(file_path_list)
    # x = reassign_numbers(mypath,sorted_list)
    # pp.pprint(x)
    # x = sorted(sorted_list, key=lambda x: x[:4])
    # pp.pprint(x)


def grab_fields_from_url(url):
    split_by_percent = url.split('%')
    eq_sign_index = split_by_percent[0].find("name=")
    start_of_name = eq_sign_index + len("name=")
    first_name = split_by_percent[0]

    pass


def parse_only_url_fields_from_file(file, names_and_locs):
    soup = BeautifulSoup(open(file, "html.parser"))
    pass


def test_main():
    pp = pprint.PrettyPrinter(indent=4)

    names_and_locs = get_names_and_locations("RA_List.xlsx")
    # pp.pprint(names_and_locs)
    param_list = gen_param_list_for_urls(names_and_locs)

    # pp.pprint(param_list)
    urls_for_num_found = gen_all_urls_for_num_found(param_list)
    print("urls_for_nums_found:")
    pp.pprint(urls_for_num_found)
    get_all_html(urls_for_num_found,"/Users/howie/PycharmProjects/webscraper/venv/html_og",False)
    print('1')
    pp.pprint(urls_for_num_found)
    mypath = "/Users/howie/PycharmProjects/webscraper/venv"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    sorted_files = sort_files_by_ascending(join(mypath,onlyfiles))
    htmls_with_nums = []
    for elem in sorted_filesfiles:
        #file = join(mypath, elem)
        soup = BeautifulSoup(open(elem), "html.parser")
        htmls_with_nums.append(soup)

    print('2')
    # print(len(htmls_with_nums))
    # pp.pprint(htmls_with_nums)
    all_num_results = get_all_num_records(htmls_with_nums)
    print('3')
    # pp.pprint(all_num_results)
    all_num_pages = get_all_num_pages(all_num_results)
    print('4')
    # pp.pprint(all_num_pages)
    all_rids = get_all_rids2(all_num_results, all_num_pages)
    print('5')
    # pp.pprint(all_rids)
    detail_urls = gen_all_urls_for_all_pages(names_and_locs,all_rids)
    with open('/Users/howie/PycharmProjects/webscraper/venv/detail_urls.txt', 'w') as f:
        for item in detail_urls:
            f.write("%s\n" % str(item))
    return detail_urls
    with open("/Users/howie/PycharmProjects/webscraper/venv/detail_urls.txt") as f:
        detail_urls = f.readlines()
    master_details_urls = detail_urls
    # you may also want to remove whitespace characters like `\n` at the end of each line
    detail_urls = []  # [x.strip() for x in detail_urls]

    detail_urls = gen_all_urls_for_all_pages(param_list, all_rids)
    print('6')
    # pp.pprint(detail_urls)

    urls = gen_all_urls(param_list)

    # urls = gen_all_urls(param_list)



    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    detail_urls = top100 = content

    # if we parse the fields from this, we can get the remaining ones
    grouped_urls = group_all_urls_by_person(param_list, detail_urls)
    print("grouped urls")
    # pp.pprint(grouped_urls)
    print("end grouped urls")
    # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # full_path_list = []
    # for file in onlyfiles:
    #    full_path_list.append(join(mypath,file))

    # reproduced_urls = []
    # for elem in full_path_list:
    #    url = reproduce_url_from_file(file)
    #    reproduced_urls.append(url)

    all_html_list = []
    for elem in grouped_urls:
        # pp.pprint("URL sublist: ")
        # pp.pprint(elem)
        htmls = get_all_html(elem, "html_folder", True)
        all_html_list.append(htmls)

    # print("grouped files by person")
    # pp.pprint(group_all_files_by_person(names_and_locs,full_path_list))
    # print("end grouped_files_by_person")
    all_html_list = grab_all_html_from_files()
    # persons = parse_all_html2(all_html_list)
    files_and_urls = []
    with open("/Users/howie/PycharmProjects/webscraper/venv/files_and_urls.txt") as f:
        files_and_urls_text = f.readlines()
        # print("FILE READ LINES")
        # print(len(files_and_urls_text))
    for file_and_url in files_and_urls_text:
        # pp.pprint(file_and_url)
        file_and_url_split = file_and_url.split(';')
        file = file_and_url_split[0]
        url = file_and_url_split[1]
        files_and_urls.append((file, url))

    # print("FILESANDURLS")
    # pp.pprint(files_and_urls)
    # print("AAAAAA")
    file_list = []
    for elem in files_and_urls:
        file_list.append(elem[0])
    url_list = []
    for elem in files_and_urls:
        url_list.append(elem[1])
    for elem in url_list:
        elem = elem.strip()
        print(elem)

    empty_urls = []
    empty_files = []
    with open("/Users/howie/PycharmProjects/webscraper/venv/empty_files.txt") as f:
        empty_files = f.readlines()

    url_list_2222 = []
    for elem in empty_files:
        if elem in files_and_urls_text:
            x = files_and_urls_text.index(elem)
            item = files_and_urls_text[x]
            item = item.split(';')[1]
            url_list_2222.append(item)
    print("ITEMITEMITEM")
    for item in url_list_2222:
        print(item)
    print("ffffffffff")
    print("jjjjjjjjjj")
    with open("/Users/howie/PycharmProjects/webscraper/venv/empty_urls.txt", "w") as f:
        for item in url_list_2222:
            f.write("%s\n" % item)

    # print("URLLIST")
    # pp.pprint(url_list)
    # print("URLLIST_LEN")
    # print(len(url_list))
    # pp.pprint(names_and_locs)

    # pp.pprint(elem[1])

    persons_list = []
    # all_html_list = flatten_list(all_html_list)
    print("go here")

    print("names_and_locs")
    print("names and locs yeah")
    # pp.pprint(names_and_locs)
    print("end")
    print("detail urls")
    print("insert detail urls")
    # pp.pprint(detail_urls)
    print("end")
    print("file_list")
    print("yep")
    # pp.pprint(file_list)
    print("end_file_list")

    persons_list = parse_all_html2(names_and_locs, all_html_list, url_list, file_list)
    # persons_list.append(persons)
    # persons_list = flatten_list(persons)

    # for elem in persons_list:
    #    print(str(elem))
    """
    test_dict = {}
    for elem in persons:
        if elem.name_searched not in test_dict.keys():
            test_dict[elem.name_searched] = [elem]
        else:
            test_dict[elem.name_searched].append(elem)

    flattened_grouped_people_list = []
    grouped_names = []
    for elem in test_dict.values():
        grouped_names.append(elem)
        for item in elem:
            flattened_grouped_people_list.append(item)

    just_names = []
    for elem in names_and_locs:
        name = elem[0]
        just_names.append(name)

    ordered_keys_and_vals = []
    for idx,name in enumerate(just_names):
        if name in test_dict.keys():
            ordered_keys_and_vals.append(test_dict[name])

    ordered_final_people = []
    for elem in ordered_keys_and_vals:
        for item in elem:
            ordered_final_people.append(item)

    print("test dict")
    pp.pprint(test_dict)
    print("end test dict")
    print("persons len")
    print(len(persons))
    print("persons begin")
    pp.pprint(persons)
    pp.pprint("End persons")

    """

    # persons = flatten_list(persons_list)
    # pp.pprint("Persons")
    # print(len(persons))
    # pp.pprint(persons)
    # pp.pprint("End persons")
    # print("6.1")
    # pp.pprint(content)

    # htmls = get_all_html(content)
    # htmls = BeautifulSoup(open("html_sample.html"), "html.parser")
    # persons = parse_all_html(htmls, names_and_locs, content)

    # person = parse_html(htmls)
    # persons = []
    # persons.append(person)

    # grouped_persons =  groupby(persons, lambda a: (a.name_searched))
    # pp.pprint(grouped_persons)
    # for elem in grouped_persons:
    #    for item in elem:
    #        print(item)
    # print(elem.name_searched)

    # grouped_persons = flatten_list(grouped_persons)

    workbook = xlsxwriter.Workbook('scraped_data.xlsx')
    print("Writing to files...")
    write_to_excel_file(persons_list, workbook)

    csv_from_excel('scraped_data.xlsx', 'scraped_data.csv')

    print("Finished.")
    # soup_list = [soup]
    # all_num_results = get_all_num_records(soup_list)
    # print('3')
    # pp.pprint(all_num_results)


def test():
    pp = pprint.PrettyPrinter(indent=4)

    mypath = "html_folder"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    pp.pprint(onlyfiles)
    full_list = []
    for elem in onlyfiles:
        full_list.append(join(mypath, elem))
    sort_files_shift_nums_and_delete_cloud_fare(onlyfiles)
    """
    for elem in onlyfiles:
        print(elem)
        soup = BeautifulSoup(open(join(mypath,elem)), "html.parser")
        cloud_fare = cloud_fare_denial_detected(soup)
        if cloud_fare:
            print("Bad File: " + basename(elem))
    """



class FileURLObj:

    def __init__(self,file,soup,num_results,num_pages,rids,first_name, last_name, city, state, middle_name, title,detail_urls):
        self.file = file
        self.soup = soup
        self.num_results = num_results
        self.num_pages = num_pages
        self.rids = rids
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.state = state
        self.middle_name = middle_name
        self.title = title
        self.detail_urls = detail_urls
        self.detail_file_url_tuples = []
        self.person_list = []

    def convert_pairings_to_string(self,pairings):
        mega_string = ''
        for elem in pairings:
            mega_string += '(' + elem[0] + "," + elem[1] + ') '
        return mega_string



    def __str__(self):
        sep = ";"
        return "[" + self.file + sep + "self.soup" + sep + str(self.num_results) +  sep + str(self.num_pages) + sep + ' '.join(self.rids) + sep + self.first_name + sep + self.last_name + sep + self.city + sep + self.state + sep + self.middle_name + sep + self.title + sep + " ".join(self.detail_urls) + sep +  self.convert_pairings_to_string(self.detail_file_url_tuples) + "\n" + " ".join(self.person_list) + "]"


def gen_detail_urls_from_og_files():
    mypath = "html_og"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    htmls_with_nums = []
    files_soup_and_num = []


    for elem in onlyfiles:
        file = join(mypath, elem)
        soup = BeautifulSoup(open(file), "html.parser")
        print("File: " + elem)
        print("Title:" + soup.find('title').get_text())
        num_results = str(get_num_results(soup))
        print("Num results:" + num_results)
        htmls_with_nums.append(soup)
        files_soup_and_num.append((file, soup, num_results))
    file_soup_num_results_num_pages = []

    for elem in files_soup_and_num:
        num_results = elem[2]
        file_soup_num_results_num_pages.append((elem[0], elem[1], num_results, get_num_pages(num_results)))
    file_soup_num_results_num_pages_rids = []
    for elem in file_soup_num_results_num_pages:
        file_soup_num_results_num_pages_rids.append((elem[0], elem[1], elem[2], elem[3], get_rids2(elem[2], elem[3])))

    names_and_locs = get_names_and_locations("/Users/howie/PycharmProjects/webscraper/venv/RA_List.xlsx")

    file_soup_num_results_num_pages_rids_name_and_loc = []
    for elem in file_soup_num_results_num_pages_rids:
        file = elem[0]
        soup = elem[1]
        num_results = elem[2]
        num_pages = elem[3]
        rids = elem[4]
        title_text = soup.find('title').getText()

        for item in names_and_locs:
            name = item[0]
            loc = item[1]
            if name in title_text:
                tuple_to_add = (file, soup, num_results, num_pages, rids, name, loc)
                if tuple_to_add not in file_soup_num_results_num_pages_rids_name_and_loc:
                    file_soup_num_results_num_pages_rids_name_and_loc.append(tuple_to_add)
    f_list = []
    file_to_write = open("/Users/howie/PycharmProjects/webscraper/venv/f_list","a")
    for elem in file_soup_num_results_num_pages_rids_name_and_loc:
        file = elem[0]
        soup = elem[1]
        num_results = elem[2]
        num_pages = elem[3]
        rids = elem[4]
        name = elem[5]
        loc = elem[6]
        param_list = gen_param_list_for_urls([[name, loc]])
        first_name, last_name, city, state, middle_name, title = param_list[0], param_list[1], param_list[2], \
                                                                 param_list[3], param_list[4], param_list[5]
        detail_urls = gen_urls_for_one_og(first_name, last_name, city, state, middle_name, title, rids)
        f = FileURLObj(file, soup, num_results, num_pages, rids, first_name, last_name, city, state, middle_name, title,
                       detail_urls)
        f_list.append(f)
        file_to_write.write(str(f))
    file_to_write.close()
    return f_list

def test_main2():
    pp = pprint.PrettyPrinter(indent=4)

    names_and_locs = get_names_and_locations("RA_List.xlsx")
    # pp.pprint(names_and_locs)
    param_list = gen_param_list_for_urls(names_and_locs)
    # pp.pprint(param_list)
    urls_for_num_found = gen_all_urls_for_num_found(param_list)

    print('1')
    # pp.pprint(urls_for_num_found)








    print('2')
    # print(len(htmls_with_nums))
    # pp.pprint(htmls_with_nums)
    #all_num_results = get_all_num_records(htmls_with_nums)
    print('3')
    # pp.pprint(all_num_results)
    #all_num_pages = get_all_num_pages_tuple(files_soup_and_num,all_num_results)
    print('4')
    # pp.pprint(all_num_pages)
    #all_rids = get_all_rids2_tuple(files_soup_and_num, all_num_results, all_num_pages)
    print('5')
    f_list = gen_detail_urls_from_og_files()
    #detail_urls = gen_all_urls_for_all_pages(names_and_locs, all_rids)
    index  = 0
    inner_index = 0
    link_to_start_at = "https://www.truepeoplesearch.com/details?name=Robin%20Brown&citystatezip=Colorado%20Springs,%20CO&rid=120x5"
    for idx,item in enumerate(f_list):
        for url in item.detail_urls:
            if link_to_start_at in url:
                index = idx
                break
            else:
                index = -1
        else:
            continue
        break

    if(index != -1):
        print(index)
        f_list = f_list[index:]
        pp.pprint(f_list[0].detail_urls)
    else:
        print("oh no")



    all_html_list = []
    skip_till = False
    for elem in f_list:
        # pp.pprint("URL sublist: ")
        # pp.pprint(elem)
        detail_urls = elem.detail_urls
        if link_to_start_at in detail_urls:
            index_of_new_start_elem = detail_urls.index(link_to_start_at) - 3
            detail_urls = detail_urls[index_of_new_start_elem:]
        htmls, detail_file_list = get_all_html(detail_urls, "/Users/howie/PycharmProjects/webscraper/venv/html_folder", True)
        elem.detail_file_url_tuples = detail_file_list
        all_html_list.append(htmls)

    file_to_write_to = open('/Users/howie/PycharmProjects/webscraper/f_after_persons.txt','a')
    persons_list = []
    for elem in f_list:
        person_list = []
        for file_url_tuple in elem.detail_file_url_tuples:
            detail_file_path = file_url_tuple[0]
            detail_url = file_url_tuple[1]
            soup = BeautifulSoup(open(detail_file_path), "html.parser")
            loc = elem.city + "," + elem.state
            #full_name = elem.first_name + " "  + elem.middle_name + " " +  elem.last_name + " "  + elem.title
            person = parse_html(soup,elem.first_name + " " + elem.last_name,loc,detail_url,detail_file_path)
            person_list.append(person)
        elem.person_list = person_list
        file_to_write_to.write(str(elem))
        persons_list.append(elem)
    file_to_write_to.close()





    #with open('detail_urls.txt', 'w') as f:
    #    for item in detail_urls:
    #        f.write("%s\n" % str(item))

    # pp.pprint(all_rids)



    #with open("detail_urls.txt") as f:
    #    detail_urls = f.readlines()
    #master_details_urls = detail_urls
    # you may also want to remove whitespace characters like `\n` at the end of each line





    # print("grouped files by person")
    # pp.pprint(group_all_files_by_person(names_and_locs,full_path_list))
    # print("end grouped_files_by_person")
    #all_html_list = grab_all_html_from_files()
    # persons = parse_all_html2(all_html_list)
    #files_and_urls = []
    #with open("files_and_urls.txt") as f:
    #    files_and_urls_text = f.readlines()
        # print("FILE READ LINES")
        # print(len(files_and_urls_text))

    #for file_and_url in files_and_urls_text:
        # pp.pprint(file_and_url)
    #    file_and_url_split = file_and_url.split(';')
    #    file = file_and_url_split[0]
    #    url = file_and_url_split[1]
    #    files_and_urls.append((file, url))

    # print("FILESANDURLS")
    # pp.pprint(files_and_urls)
    # print("AAAAAA")
    #file_list = []
    #for elem in files_and_urls:
    #    file_list.append(elem[0])
    #url_list = []
    #for elem in files_and_urls:
    #    url_list.append(elem[1])
    #for elem in url_list:
    #    elem = elem.strip()
    #    print(elem)

    #empty_urls = []
    #empty_files = []
    #with open("empty_files.txt") as f:
    #    empty_files = f.readlines()

    #url_list_2222 = []
    #for elem in empty_files:
    #    if elem in files_and_urls_text:
    #        x = files_and_urls_text.index(elem)
    #        item = files_and_urls_text[x]
    #        item = item.split(';')[1]
    #        url_list_2222.append(item)
    #print("ITEMITEMITEM")
    #for item in url_list_2222:
    #    print(item)
    #print("ffffffffff")
    #print("jjjjjjjjjj")
    #with open("empty_urls.txt", "w") as f:
    #    for item in url_list_2222:
    #3        f.write("%s\n" % item)



    # pp.pprint(elem[1])

    #persons_list = []
    # all_html_list = flatten_list(all_html_list)
    print("go here")

    print("names_and_locs")
    print("names and locs yeah")
    # pp.pprint(names_and_locs)
    print("end")
    print("detail urls")
    print("insert detail urls")
    # pp.pprint(detail_urls)
    print("end")
    print("file_list")
    print("yep")
    # pp.pprint(file_list)
    print("end_file_list")


    #persons_list = parse_all_html2(names_and_locs, all_html_list, url_list, file_list)





    workbook = xlsxwriter.Workbook('scraped_data.xlsx')
    print("Writing to files...")

    write_to_excel_file(persons_list, workbook)

    csv_from_excel('scraped_data.xlsx', 'scraped_data.csv')

    print("Finished.")



if __name__ == '__main__':
    #test_main2()
    pp = pprint.PrettyPrinter(indent=4)
    bad_file_url_pairs = get_bad_file_url_pairs()
    pp.pprint(bad_file_url_pairs)
    #detail_urls = test_main()
    #for elem in detail_urls:
    #    print("url: " + str(elem))
    #pp.pprint(detail_urls)
    """
    pp = pprint.PrettyPrinter(indent=4)

    names_and_locs = get_names_and_locations("RA_List.xlsx")

    # pp.pprint(names_and_locs)
    param_list = gen_param_list_for_urls(names_and_locs)
    # pp.pprint(param_list)
    urls_for_num_found = gen_all_urls_for_num_found(param_list)
    for elem in urls_for_num_found:
        print(elem)
    #pp.pprint(urls_for_num_found)
    #test_main()
    """
# Notes
# Discard Full Background Report/Background Report
