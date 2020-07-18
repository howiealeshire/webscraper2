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
    soup = BeautifulSoup(open("html_sample.html"), "html.parser")
    parent_results = soup.findAll('div', class_="col-12 col-sm-11")

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

    def get_age_and_year(original_soup):
        results = original_soup.find('div', class_="row pl-md-2")
        results = remove_line_break_and_concat(results.find('span', class_="content-value"))
        pp.pprint(results)
        #for elem in results.children:
        #    pp.pprint(elem)
       # pp.pprint(results)
        return results
    age_and_year = get_age_and_year(soup).split()
    age = age_and_year[1]
    year = age_and_year[2] + " " + age_and_year[3]
    year = year.replace("(","")
    year = year.replace(")","")
    print("Age")
    print(age)
    print("Year")
    print(year)

    def get_address(soup):
        address_html = soup[0].find('a', class_="link-to-more olnk")
        return remove_line_break_and_concat(address_html)

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

    def make_parent_child_list(parent_soup):
        result_list = []
        intermediate_list = []
        for parent in parent_soup:
            #intermediate_list.append(parent)
            for child in parent.children:
                intermediate_list.append(child)
            result_list.append(intermediate_list)
            intermediate_list = []
        return result_list

    parent_child_list = make_parent_child_list(parent_results)

    print(">>>>>>>>>>>>>>>")
    num_list = []
    #pp.pprint(parent_child_list)
    unparsed_numbers = parent_child_list[1]

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


    pp.pprint(list_without_emptys)
   # pp.pprint(num_list)
    #yyyy = get_link_value(parent_child_list[1],3)

    print("fjdljlfldjflsjslj------------")

    #for elem in xz:
     #   for y in elem:
      #      print(y)
      #  print("hhhhhhhhhhhhhhhhhhhhhddhdhdhdhdhdhdhdhdhdhdhdhdhdhd")

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



#Notes
#Discard Full Background Report/Background Report