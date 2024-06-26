import os
import requests
import datetime as dt
from multiprocessing import Pool
try:
    from bs4 import BeautifulSoup
except:
    #try again
    try:
        os.system("python3 -m pip install beautifulsoup4")
        os.system("python3 -m pip install bs4")
        from bs4 import BeautifulSoup
    except:
        os.system("python -m pip install beautifulsoup4")
        os.system("python -m pip install bs4")
        from bs4 import BeautifulSoup
        #try yet again
        try:
            os.system("py -m pip install beautifulsoup4")
            os.system("py -m pip install bs4")
            from bs4 import BeautifulSoup
        except:
            os.system("easy_install beautifulsoup4")
            os.system("easy_install bs4")
            from bs4 import BeautifulSoup

html_tags = ["html", "head", "body", "title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "img", "ul", "ol", "li", "div", "span",
              "abbr", "address","area", "article","aside","audio","base","bdi","bdo","blockquote","button","canvas","caption","cite",
              "code","col","colgroup","data","datalist","dd","del","details","dfn","dialog","dl","dt","em","embed","fieldset","figcaption",
              "figure","footer","form","header","hgroup","hr","i","iframe", "input", "ins","kbd","label","legend","link","main","map",
              "mark","menu", "meta","meter","nav","noscript","object","optgroup", "option","output","param","picture","pre","progress","q",
              "rp","rt", "ruby","s","samp","script","search","section","select","small","source","strong","style","sub","summary","sup","svg",
              "table","tbody","td","template","textarea","tfoot","th","thread","time","tr","track","u","var","video","wbr"]

# if the website you're trying to archive has a / at the end, please remove it.
# e.g: turn https://google.com/ into https://google.com
url = "https://google.com"

#save folder path
save_timestamp = f"{dt.date.today()}-{dt.datetime.now().hour}-{dt.datetime.now().minute}-{dt.datetime.now().second}"
save_folder_p = url.split("//")[1]+ "-" + save_timestamp

content = requests.get(url).text
soup = BeautifulSoup(content,"html.parser")

#gets all sources to links
def getAllSrc(html_tags, soup, save_folder_p):
    all_src = []
    for i in range(len(html_tags)):
        all_of_element = soup.find_all(html_tags[i])
        for el in all_of_element:
            src = el.get("src")
            if src == None:
                continue
            else:
                link = requests.compat.urljoin(url,src)
                all_src.append(link)
                local_src_path = downloadSource(src, save_folder_p)
                soup.replace(src,f"archived_websites/{save_folder_p}/{local_src_path}")
    return all_src

#gets all hrefs
def getAllHref(html_tags,soup,save_folder_p):
    all_href = []
    for i in range(len(html_tags)):
        all_of_element = soup.find_all(html_tags[i])
        for el in all_of_element:
            href = el.get("href")
            if href == None:
                continue
            else:
                link = requests.compat.urljoin(url,href)
                all_href.append(link)
                local_href_path = downloadSource(href, save_folder_p)
                soup.replace(href,f"archived_websites/{save_folder_p}/{local_href_path}")
    return all_href

def downloadSource(file_to_save, save_folder_p):
    r = requests.get(f"{url}{file_to_save}")
    with open(f"{save_folder_p}/{file_to_save}", "wb") as f:
        f.write(r.text)
    return f"{save_folder_p}/{file_to_save}"

sources = getAllSrc(html_tags,soup,save_folder_p)
hrefs = getAllHref(html_tags,soup,save_folder_p)

#writes all sources to folder named after url
try:
    os.mkdir(f"archived_websites/{save_folder_p}")
except:
    print("directory already exists")
    pass

with open(f"archived_websites/{save_folder_p}/href.txt", "a") as f:
    for i in range(len(hrefs)):
        f.write(f"{hrefs[i]}\n" )

with open(f"archived_websites/{save_folder_p}/src.txt", "a") as f:
    for i in range(len(sources)):
        f.write(f"{sources[i]}\n")

with open(f"archived_websites/{save_folder_p}/index.html", "w") as f:
    f.write(content)

save_path = f"archived_websites/{save_folder_p}/sources"

try:
    os.mkdir(save_path)
except:
    pass

for i in range(len(sources)):
    item = requests.get(sources[i])
    if item.status_code == 200:
        with open(f"{save_path}", "wb") as f:
            f.write(item.content)
            print(f"file {i} successfully downloaded")
    else:
        print(f"file {i} failed")



# TO-DO:
#  - Add scraping debth (default 2 or 3?)so some links are also scraped along the index page.
#  - When searching the 'soup' for links, add them to list, and replace them 
#    with path in local dierectory instead of original website.
#  - When all links replaced, create folder with all the href resources and src resources
#    and keep href and src seperate.
#  - When its a href, and a html page, save the page and perform the scraping on that one too,
#    as long as it is less or equal to the depth of saving (not sure that makes sense).