from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import pprint



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

def get_html_from_page(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }

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
    request = urllib.request.Request(video_url, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()  # The data u need
    soup = BeautifulSoup(data, 'html.parser')
    return soup
    #print(data)
    # page = urllib.request.urlopen(video_url)
    # soup = BeautifulSoup(page, 'html.parser')
    # print(soup)

    #f = open("html_sample.txt", "w")
    #f.write(soup.prettify())
    #f.close()
    #print(soup.prettify())


def parse_html(html):
    soup = BeautifulSoup(open("html_sample.html"), "html.parser")
    #results = soup.findAll('div', class_="content-label h5")
    parent_results = soup.findAll('div', class_="col-12 col-sm-11")
    current_address = parent_results[0].find('a', class_="link-to-more olnk")
   # print(div.find('a')['href'])
    for x in current_address.contents:
        print(x)
    #print(current_address)
    #current_address_text = current_address.text()
    #print(current_address_text)
    #print(parent_results[0].prettify())
    #for h in results:
        #print(h.prettify())
    #results_content = soup.findAll('div', class_="content-value")
    #for a in results_content:
    #    print(a.prettify())
    #print(results.prettify())

def main():
    pass


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    #names_and_locs = get_names_and_locations("/Users/howie/Downloads/RA_List.xlsx")
    #param_list = gen_param_list_for_urls(names_and_locs)
    #pp.pprint(param_list)
    #x = gen_all_urls(param_list)
    #pp.pprint(x)
    #get_html_from_page("")
    parse_html("")




   # print("hello")
