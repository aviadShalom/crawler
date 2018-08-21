import cfg
import urllib2
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import re
import datetime
import json


currect_workers = 0
cached_url = []
def crawler_main(main_url,match_words,recursion_depth):
    results = []
    cached_url = load_url_data()
    for item in match_words:
        results.append({"word":item,"count":0})

    domain_name = get_domain_name(main_url)

    if currect_workers < cfg.NUM_PAGE_EXTRAXcTOR_WORKERS:
        crawler_process(main_url,recursion_depth,results, 0,domain_name)
        #save_data()
        print results
        return results

    else:
        #TODO: implemet waiting for free worker
        return "Busy"


def crawler_process(page_url, recursion_depth,results,currect_depth,domain):
    currect_depth = currect_depth +1
    if currect_depth > recursion_depth:
        return

    page_data = extract_page(page_url)
    page_text = extract_page_text(page_data)
    child_links = find_all_child_links(page_data,domain)

    #save_url(page_url,page_text,child_links)

    find_words_in_url(page_text, results)
    if (currect_depth + 1) > recursion_depth:
        return

    for link in child_links:
        #TODO: execute in a different thread
        crawler_process(link,recursion_depth,results,currect_depth,domain)

def extract_page(url):
    try:
        page = urllib2.urlopen(url)
        soap = BeautifulSoup(page)
        return soap

    except Exception as e:
        print e.message
        return None


def find_all_child_links(page_data,domain):
    links = page_data.findAll('a', href=True)

    child_links = []
    for link_item in links:
        #TODO: remove external urs
        link = validate_child_link(link_item['href'],domain)
        if link is not None:
            child_links.append(link)
    if cfg.DEBUG:
        return child_links[:5]
    else:
        return child_links


def extract_page_text(page_data):
    p_list = page_data.findAll('p')
    p_data = ''
    for p in p_list:
        p_data = p_data + ' ' +  re.sub(r'<.+?>', r'', str(p))

    #p_data = [re.sub(r'<.+?>', r'', str(a)) for a in p_list]

    return p_data

def validate_child_link(link,domain):
    if 'http' in link:
        if domain in link:
            return link
        else:
            return None
    else:
        return domain + link


def find_words_in_url(page_text,results):

    for word in results:
        word['count'] = word['count'] + page_text.count(word['word'])


def get_domain_name(page_url):
    parsed_uri = urlparse(page_url)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result[:-1]


def save_url(page_url,page_data,child_links):

    data = {"page_url":page_url,"page_data":page_data,"child_links":child_links,"data_date":datetime.datetime.now()}
    cached_url.append(data)


def save_data():
    with open(cfg.CACHED_URL_FILE_NAME, 'w') as outfile:
        json.dump(cached_url, outfile)

def load_url_data():
    with open(cfg.CACHED_URL_FILE_NAME) as f:
        data = json.load(f)
    return data