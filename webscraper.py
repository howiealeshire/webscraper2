from bs4 import BeautifulSoup
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
import os

class Person:
    def __init__(self,bus,name_searched,loc_searched,details_url,tps_name,tps_age,birth_date,
                 curr_address,phone_nums,email_addresses,prev_addresses,possible_buses_and_addresses,bus_dates,prev_address_dates):
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

    def __str__(self):
        separator = ","
        return self.bus + "," + self.name_searched + "," + self.loc_searched + "," + self.details_url + "," + self.tps_name + "," + self.tps_age +  "," + self.birth_date + "," + self.curr_address  + "," + separator.join(self.phone_nums) + "," + separator.join(self.email_addresses)  + "," + separator.join(self.prev_addresses) + "," + separator.join(self.possible_buses_and_addresses)

def get_names_and_locations(file_path):
    df = pd.read_excel(file_path)
    names_and_locs = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
    #names_and_locs2 = [names_and_locs[0],names_and_locs[1],names_and_locs[2],names_and_locs[3],names_and_locs[4],names_and_locs[5]]
    return names_and_locs

def gen_url(first_name, last_name, city, state):
    test_url = "https://www.truepeoplesearch.com/details?name=John%20Smith&citystatezip=Atlanta%2C%20GA&rid=0x0"
    template_url = "https://www.truepeoplesearch.com/details?name=" + first_name + "%20" + last_name + "&citystatezip=" + city + "%2C%20" + state +  "&rid=0x0"
    return template_url

def gen_all_urls(names_and_locs):
    url_list = []

    for elem in names_and_locs:
        url = gen_url(elem[0],elem[1],elem[2],elem[3])
        url_list.append(url)
    return url_list

def gen_param_list_for_urls(names_and_locs):
    gen_list = []
    for idx, val in enumerate(names_and_locs):
        first_name = names_and_locs[idx][0].split()[0]
        last_name = names_and_locs[idx][0].split()[1]
        city = names_and_locs[idx][1].split()[0]
        city = city.replace(',', '')
        state = names_and_locs[idx][1].split()[1]
        elem_to_add = [first_name,last_name, city,state]
        gen_list.append(elem_to_add)
    return gen_list

def get_html_from_page(video_url):

    #user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    #user_agent = 'your bot 0.2222'
    #headers = {'User-Agent': user_agent, }


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
    #proxy_ip = FreeProxy().get()

    #proxy = urllib2.ProxyHandler({"http": proxy_ip})
    #opener = urllib2.build_opener(proxy)
    #opener.addheaders = [('User-Agent',user_agent)]
    #urllib2.install_opener(opener)

    #req = urllib.request.Request(video_url)
    #req.add_header('User-Agent', user_agent)
    #page = urllib.request.urlopen(req)

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random}
    result = requests.get(video_url, headers=headers)
    #"http://webcache.googleusercontent.com/search?q=cache:"
    #pp.pprint(page.info())
    #request = urllib.request.Request(video_url, None, headers)  # The assembled request
    #response = urllib.request.urlopen(request)

    data = result.text  # The data u need
    #pp.pprint(data)
    soup = BeautifulSoup(data, 'html.parser')

    time.sleep(25) #to prevent captcha

    return soup
    #print(data)
    # page = urllib.request.urlopen(video_url)
    # soup = BeautifulSoup(page, 'html.parser')
    # print(soup)

    #f = open("html_sample.txt", "w")
    #f.write(soup.prettify())
    #f.close()
    #print(soup.prettify())


def parse_html(soup,name_searched='',loc_searched='',url=''):
    pp = pprint.PrettyPrinter(indent=4)
    """
      address = get_address(parent_results)
      for x in parent_results:
          if x == "Phone Numbers":
              print(x)
      print(get_link_value(parent_results,4))

      current_address = parent_results[0]
     # print(div.find('a')['href'])
      for x in current_address.contents:
          print("hello")
          #print(x)
      #print(current_address)
      #current_address_text = current_address.text()
      #print(current_address_text)
      for y in parent_results:
          print(y.prettify())
      #print(parent_results.prettify())
      #for h in results:
          #print(h.prettify())
      #results_content = soup.findAll('div', class_="content-value")
      #for a in results_content:
      #    print(a.prettify())
      #print(results.prettify())
      """
    #soup = BeautifulSoup(html, "html.parser")
    parent_results = soup.findAll('div', class_="col-12 col-sm-11")
    def make_parent_child_list(parent_soup):
        result_list = []
        intermediate_list = []
        for parent in parent_soup:
            # intermediate_list.append(parent)
            for child in parent.children:
                intermediate_list.append(child)
            result_list.append(intermediate_list)
            intermediate_list = []
        return result_list
    #accepts html
    def remove_line_break_and_concat(html_elem):
        html_elem = str.split(html_elem.get_text())
        parsed_text_full = ""
        if "<br>" in html_elem:
            html_elem.remove(html_elem.index("<br>"))
        for elem in html_elem:
            parsed_text_full += elem + " "
        parsed_text_full = parsed_text_full.strip()
        return parsed_text_full
    def get_value_title(soup, title):
        x = soup.find(text=re.compile(title))
        #pp.pprint(x.parent.parent.parent.parent.children)
        return x.parent.parent.parent.parent.children


        #for elem in soup:
            #pp.pprint(elem)

        #soup = soup.find('div', class_="content-label h5")
        #soup2 = BeautifulSoup(open("html_sample.html"), "html.parser")
        #soup2 = soup2.find('div', class_="content-label h5")

        #pp.pprint(soup2)
    def get_name_age_and_year(original_soup):
        results = original_soup.find('div', class_="row pl-md-2")
        if results is not None:
            name = results.find('span', class_="h2")
            name = remove_line_break_and_concat(name)
            results = remove_line_break_and_concat(results.find('span', class_="content-value"))
            if results is not None:
                age_and_year = results.split()
            if(len(age_and_year) > 0):
                age = age_and_year[1]
            else:
                age = ['','']
            if(len(age_and_year) > 3):
                year = age_and_year[2] + " " + age_and_year[3]
                year = year.replace("(", "")
                year = year.replace(")", "")
            else:
                year = ''

        else:
            name = ''
            age = ''
            year = ''

        return name,age,year
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
    def get_link_value(soup):
        html_doc = soup.findAll('a', class_="link-to-more olnk")
        num_list = []
        for elem in html_doc:
            if elem is not None:
                elem = elem.get_text()
                elem = elem.replace('\n', "").strip()
                num_list.append(elem)

        """
        if html_doc is not None:

        if html_doc is not None:

        """
        return num_list
    def parse_bus(bus):
        l = []
        text_bus = bus.get_text()
        #pp.pprint("text bus")
        #pp.pprint(text_bus)
        #pp.pprint("</text bus>")
        #pp.pprint(bus.get_text())
        text_bus_trimmed = bus.get_text().split("\n")
        trimmed_l = []
        if text_bus_trimmed is not None:
            for idx,elem in enumerate(text_bus_trimmed):
                if elem.strip() != '':
                    trimmed_l.append(elem.strip())
                    #pp.pprint("text bus trimmed")
                    #pp.pprint(text_bus_trimmed[idx])
        for elem in trimmed_l:
            l.append(elem)
        #l_to_add = text_bus_trimmed
        #pp.pprint(l)
        #pp.pprint("LLL")
        #pp.pprint(l)
        #pp.pprint("LLLLL")
        return l

    def parse_vals_true(sub_soup,is_bus=False, get_dates=False):
        unparsed_emails_true = sub_soup.findAll('div', class_="content-value")
        #pp.pprint(unparsed_emails_true)
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
                        date_list.append('')
                #pp.pprint("email list parsed")
                email_list_parsed.append(remove_line_break_and_concat(elem))
                #pp.pprint(email_list_parsed)
            else:
                if elem is not None:
                    date = elem.find('span', class_="content-label smaller")
                    if date is not None:
                        date_list.append(date)
                    else:
                        date_list.append('')
                    l_to_add = parse_bus(elem)
                    #pp.pprint("L to add")
                    #pp.pprint(l_to_add)
                    email_list_parsed.append(l_to_add)
                    #email_list_parsed.append(l_to_add)
        if get_dates == True:
            #pp.pprint("DATE LIST")
            #pp.pprint(date_list)
            #pp.pprint("END DATE LIST")
            return email_list_parsed,date_list
        else:
            return email_list_parsed
    def get_index_of_elem(parent_soup,needle):
        for idx, elem in enumerate(parent_soup):
            unparsed_emails_true = elem.find('div', class_="content-label h5")
            #pp.pprint(parent_soup[4].getText())
            #pp.pprint(unparsed_emails_true.getText())
            if(needle in unparsed_emails_true.getText()):
                return idx

        return -1

    def parse_buses_true(sub_soup):
        unparsed_emails_true = sub_soup.findAll('div', class_="content-value")
        #pp.pprint(unparsed_emails_true)
        email_list_parsed = []
        for elem in unparsed_emails_true:
            if elem is not None:
                l_to_add = parse_bus(elem)
                for item in l_to_add:
                    email_list_parsed.append(item)

        return email_list_parsed

    name,age,year = get_name_age_and_year(soup)

    if parent_results is not None:
        idx = get_index_of_elem(parent_results,"Email Addresses")
        if idx is not -1:
            parsed_emails_true = parse_vals_true(parent_results[idx])
        else:
            parsed_emails_true = []
    else:
        parsed_emails_true = []
    #pp.pprint(parsed_emails_true)
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

   # pp.pprint(parsed_addresses_true)
    if parent_results is not None:
        idx = get_index_of_elem(parent_results,"Possible Businesses")
        if idx is not -1:
            parsed_buses_true,parsed_bus_dates_true = parse_vals_true(parent_results[idx],True,True)
        else:
            parsed_buses_true = []
            parsed_bus_dates_true = []
    else:
        parsed_buses_true = []
        parsed_bus_dates_true = []

    def parse_values(unparsed_numbers):
        num_list = []
        for val in unparsed_numbers:
            if val is not None and val != '\n':
                x = get_link_value(val)
                if x is not None:
                    num_list.append(x)
        list_without_emptys = []
        for elem in num_list:
            for item in elem:
                if len(elem) is not 0:
                    list_without_emptys.append(item)
        return  list_without_emptys

    if parent_results is not None:
        idx = get_index_of_elem(parent_results,"Phone Numbers")
        #pp.pprint(idx)
        if idx is not -1:
            parsed_numbers =  parse_vals_true(parent_results[idx],False,False)
        else:
            parsed_numbers = []
    else:
        parsed_numbers = []

    #pp.pprint(parsed_buses_true)
    curr_address = get_address(parent_results)
    #print("curr address:")
   # pp.pprint(curr_address)

    #parent_child_list = make_parent_child_list(parent_results)
    #print(">>>>>>>>>>>>>>>")






    #print("????")
#    parsed_numbers = parse_values(unparsed_numbers)
    #pp.pprint(parsed_numbers)

    #print("fjdljlfldjflsjslj------------")
    bus_date = ''
    #print("parsed buses")
    #pp.pprint(parsed_buses_true)
    #print("close")
    if parsed_buses_true is not None and len(parsed_buses_true) > 0:
        default_business = ''.join(parsed_buses_true[0])
    else:
        default_business = ''
    p = Person(default_business,name_searched,loc_searched,url,name,age,year,curr_address,parsed_numbers
                          ,parsed_emails_true,parsed_addresses_true,parsed_buses_true,parsed_bus_dates_true,parsed_address_dates_true)
    return p
    #for elem in xz:
     #   for y in elem:
      #      print(y)
      #  print("hhhhhhhhhhhhhhhhhhhhhddhdhdhdhdhdhdhdhdhdhdhdhdhdhd")

def main():
    pass


def get_all_html(urls):
    html_list = []
    for elem in urls:
        html_list.append(get_html_from_page(elem))
        print("Got html from: " + str(elem))
    print("Scraped all html.")
    return html_list

def parse_all_html(htmls,names_and_locs,urls):
    person_list = []
    for idx,html in enumerate(htmls):
        name_and_loc = names_and_locs[idx]
        name = name_and_loc[0]
        loc = name_and_loc[1]
        url = urls[idx]
        person = parse_html(html,name,loc,url)
        person_list.append(person)
        print("Parsed:" + " " + str(person.bus) + "," + str(person.name_searched) + ", " + str(person.loc_searched))
    return person_list

def write_to_excel_file(persons, workbook):
    worksheet = workbook.add_worksheet()
    row = 1
    col = 0
    header_row = 0
    worksheet.write(header_row,col,"Business")
    worksheet.write(header_row,col+1,"Name")
    worksheet.write(header_row,col+2,"Location")
    worksheet.write(header_row,col+3,"Truepeopleurl")
    worksheet.write(header_row,col+4,"TPS Name")
    worksheet.write(header_row,col+5,"TPS Age")
    worksheet.write(header_row,col+6,"TPS Birth Month and Year")
    worksheet.write(header_row,col+7,"TPS Current Address")

    i = 0
    while i < 100:
        worksheet.write(header_row, col + 8+i, "TPS Phone Number" + " " + str(i+1))
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
    #col1 = col
    #col2 = col
    while j < 300:
        worksheet.write(header_row, col + j, "Possible_Business_"  + str(num_index))
        j += 1
        worksheet.write(header_row, col + j, "Possible_Business_Address_"  + str(num_index))
        j += 1
        worksheet.write(header_row, col + j, "Possible_Business_Address_"  + str(num_index) + " Date")
        j += 1
        num_index += 1


    #worksheet.write(header_row,col+9,"TPS Age")
    #worksheet.write(header_row,col+10,"TPS Age")
    row = 1
    col = 0
    for person in persons:
        worksheet.write(row, col, person.bus)
        worksheet.write(row, col + 1, person.name_searched)
        worksheet.write(row,col+2,person.loc_searched)
        worksheet.write(row,col+3,person.details_url)
        worksheet.write(row,col+4,person.tps_name)
        worksheet.write(row,col+5,person.tps_age)
        worksheet.write(row,col+6,person.birth_date)
        worksheet.write(row,col+7,person.curr_address)
        col = col + 8
        i = 0
        for idx,elem in enumerate(person.phone_nums):
            worksheet.write(row,col+i,elem)
            i += 1
        col = 108
        i = 0
        for idx,elem in enumerate(person.email_addresses):
            worksheet.write(row,col+idx,elem)
            i = idx
        col = 208
        i = 0
        for idx,elem in enumerate(person.prev_addresses):
            worksheet.write(row,col+i,elem.split('(')[0])
            i += 1
            #print("prev address_Dates to write")
            #pp.pprint(person.prev_address_dates[idx])
            #print("end prev aaddress dates to write")
            worksheet.write(row,col+i,person.prev_address_dates[idx])
            i += 1

        col = 408
        i = 0
        for idx, elem in enumerate(person.possible_buses_and_addresses):
            #print("elem")
            #pp.pprint(elem)
            #print("</elem>")
            worksheet.write(row, col + i, elem[0])
            i += 1
            worksheet.write(row,col+i,elem[1])
            i += 1
            #pp.pprint("DATES")
            #pp.pprint(person.bus_dates)
            #pp.pprint("ENDDATES")
            worksheet.write(row,col+i,person.bus_dates[idx])#person.bus_dates[idx])
            i += 1

        col = 708
        i = 0
        row += 1
        col = 0
    workbook.close()

def csv_from_excel(workbook_path,csv_output_file_path):
    wb = xlrd.open_workbook(workbook_path)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(csv_output_file_path, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

if __name__ == '__main__':
    #csv_from_excel('/Users/howie/Desktop/scraped_data.xlsx','tps_extracted_data.csv')

    pp = pprint.PrettyPrinter(indent=4)
    names_and_locs = get_names_and_locations("RA_List.xlsx")
    #pp.pprint(names_and_locs)
    param_list = gen_param_list_for_urls(names_and_locs)
    #pp.pprint(param_list)
    urls = gen_all_urls(param_list)
    htmls = get_all_html(urls)
    #htmls = BeautifulSoup(open("html_sample.html"), "html.parser")
    persons = parse_all_html(htmls,names_and_locs,urls)

    #person = parse_html(htmls)
    #persons = []
    #persons.append(person)

    workbook = xlsxwriter.Workbook('scraped_data.xlsx')
    print("Writing to files...")
    write_to_excel_file(persons,workbook)
    
    
    

    csv_from_excel('scraped_data.xlsx', 'scraped_data.csv')
    os.remove("scraped_data.xlsx")
    print("Finished.")

    #os.remove("scraped_data.xlsx") --Enable at end.

    #for elem in persons:
     #   pp.pprint(str(elem))
    #with open('your_file.txt', 'w') as f:
     #   for item in persons:
      #      f.write("%s\n" % str(item))
    #pp.pprint(x)

    #f = open("demofile2.txt", "a")
    #f.write("Now the file has more content!")
    #f.close()
    #get_html_from_page("")
    #parse_html("")




   # print("hello")



#Notes
#Discard Full Background Report/Background Report