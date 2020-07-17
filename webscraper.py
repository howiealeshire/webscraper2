from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import pprint
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}


video_url = "https://www.truepeoplesearch.com/details?name=John%20Smith&citystatezip=Atlanta%2C%20GA&rid=0x0"

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
request=urllib.request.Request(video_url,None,headers) #The assembled request
#soup = BeautifulSoup(html_doc, 'html.parser')
response = urllib.request.urlopen(request)
data = response.read() # The data u need
print(data)
#page = urllib.request.urlopen(video_url)
#soup = BeautifulSoup(page, 'html.parser')
#print(soup)
#print(soup.prettify())


def get_names_and_locations(file_path):
    df = pd.read_excel(file_path)
    names_and_locs = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
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

def main():
    pass


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    names_and_locs = get_names_and_locations("/Users/howie/Downloads/RA_List.xlsx")
    param_list = gen_param_list_for_urls(names_and_locs)
    #pp.pprint(param_list)
    x = gen_all_urls(param_list)
    pp.pprint(x)





   # print("hello")
