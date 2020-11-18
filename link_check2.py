import requests
import validators
import pprint
import re
from logzero import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)
root_url = 'https://www.nyrr.org' # This should be the hostname / root URL as we will be appending to it later.
rule = re.compile(r"^[\w\/\.\-]+$")
visited = {}

# Master function (one function to rule them all)
def crawl_website(depth, url):
    if visited.get(url):
        return
    depth = depth + 1
    # Create a short-circuit here for testing.
    if depth >= 3:
        print('gotten to maximum recursive depth: {}'.format(depth))
        logger.info('-------[We are not checking this: %s url]------', url)
        return
    if check_url(url):
        logger.info('Check URL returned True')   
        found_links = get_links(get_html(url))        
        horizon = add_new_links_to_horizon(found_links)     
        for u in horizon:
            print('Key: {}'.format(u))
            crawl_website(depth, u)
    logger.info('You\'ve reached the end of the list! Cheers!')
    # pprint.pprint(horizon)    

def check_url(url):
    if url is not None and check_rules(url):
        return True        
    logger.info('All the rules didn\'t pass')
    return False

def get_html(url):
    page = requests.get(url)
    visited[url] = page.status_code
    if (page.status_code >= 200 and page.status_code < 300) and page.headers['Content-Type'] == 'text/html; charset=utf-8':        
        page_html = BeautifulSoup(page.text, 'html.parser')            
        return page_html
    logger.info('The get_html function failed')    

def get_links(url):
    if url is None:
        return
    current_page_links = {}
    for link in url.find_all('a'):
        if link != url:
            current_page_links[link.get('href')] = [False, '', '']
    return current_page_links

def add_new_links_to_horizon(current_page_links):
    horizon = []
    if current_page_links is not None:
        for url in current_page_links.keys():
            full_url = urljoin(root_url, url)
            if url is not None and len(url) > 4 and check_rules(url):
                horizon.append(full_url)
    return horizon

def check_rules(url):
    u = re.sub(root_url, '', url)
    print("checking url: {}".format(u))
    if rule.match(u) is not None or u == "":
        return True
    return False

crawl_website(0, root_url)

for v in visited:
    print("{} => {}\n".format(v, visited[v]))