import requests
import validators
import pprint
from logzero import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)
root_url = 'https://www.nyrr.org' # This should be the hostname / root URL as we will be appending to it later.
horizon = {
    root_url : [False, 200],
}

# Master function (one function to rule them all)
def crawl_website():
    for url in list(horizon): # I think this might be where it is failing. The list never updates with the new URLs on the second pass. 
        logger.info('-------[We are not checking this: %s url]------', url)
        if check_url(url):
            logger.info('Check URL returned True')
            found_html = get_html(url)        
            found_links = get_links(found_html)        
            add_new_links_to_horizon(found_links)
            
            logger.info('Key: %s', url)
            # logger.info('horizon: %s', horizon)
            if horizon[url][0] == False:
                logger.info('horizon[url][0] == False:)')
                crawl_website()
            elif horizon[url][0] == True:
                logger.info('horizon[url][0] == False:)')
                pass
            else:
                logger.info('There was some kind of error in the checked_value check')
    logger.info('You\'ve reached the end of the list! Cheers!')
    # pprint.pprint(horizon)    

def check_url(url):
    logger.info('The checked value of %s is %s' % (url, horizon[url][0]))
    if  url == root_url:
        return True
    elif url != None and check_rules(url[20:]):
        return True
    else:
        horizon[url] = [True, 'bad url', 'bad url']            
        logger.info('All the rules didnt pass')
        return False

def get_html(url):
    page = requests.get(url)
    if page.status_code == 200 and page.headers['Content-Type'] == 'text/html; charset=utf-8':        
        horizon[url] = [True, page.status_code, page.headers['Content-Type']] #Why isn't this happening?
        page_html = BeautifulSoup(page.text, 'html.parser')            
        return page_html
    else:
        horizon[root_url + url] = [True, page.status_code, page.headers['Content-Type']]
        logger.info('The get_html function failed')    

def get_links(url):
    current_page_links = {}
    for link in url.find_all('a'):
        if link != url:
            current_page_links[link.get('href')] = [False, '', '']
    return current_page_links

def add_new_links_to_horizon(current_page_links):
    for url in current_page_links.keys():
        full_url = urljoin(root_url, url)
        if url != None and len(url) > 4 and check_rules(url):
            if full_url not in horizon:
                logger.info('This url is being added to the horizon: %s', full_url)
                horizon[full_url] = [False, '', '']

def check_rules(url):
    rules = [
            url != None,
            url != '/',
            url != '',
            url[0:10] != 'link.aspx?',
            url[0:3] != 'tel',
            url != '/~',
            url != '#',
            url[0:10] != 'javascript',            
            url[0:4] != 'http',
            url[0:6] != 'mailto'
        ]
    
    # print('The URL %s returned %r to the rule check' % (url, all(rules)))
    if all(rules):
        return True
    else:
        return False  

crawl_website()