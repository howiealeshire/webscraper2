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
    pp = pprint.PrettyPrinter(indent=4)
    df = pd.read_excel(file_path)
    pp.pprint(df.to_dict())
    x = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
    #return_list = ex_data['column1_name'].values.tolist()
    return_list = []
    return x

def main():
    pass

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    names_and_locs = get_names_and_locations("/Users/howie/Downloads/RA_List.xlsx")
    pp.pprint(names_and_locs)
    print("hello")
