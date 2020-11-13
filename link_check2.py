import requests
import validators
import pprint
from logzero import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)
root_url = 'https://www.nyrr.org' # This should be the hostname / root URL as we will be appending to it later.
horizon = {
    root_url : [False, '', ''] # [has been checked, status code, content type]
}

# Master function (one function to rule them all)
def crawl_website(url):
    logger.info('Currently checking: %s', url)
    check_for_new_links(get_links(check_url(url)))
    next_link = next(iter(horizon))
    logger.info('The next link to check will be: %s', next_link)
    # crawl_website(next_link) # grab the next item in the horizon # I think this is broken / not grabbing the next link. Maybe an iterator?
    pprint.pprint(horizon)

def check_url(url):
    logger.info('Made it to the check_url function')
    logger.info('The checked value of %s is %s' % (url, horizon[url][0]))
    if horizon[url][0] == False:
        if check_rules(url):
            logger.info('All rules passed?')
            page = requests.get(url)
            if page.status_code == 200 and page.headers['Content-Type'] == 'text/html; charset=utf-8':
                logger.info('%s is an HTML page and returned a 200', url)
                horizon[url] = [True, page.status_code, page.headers['Content-Type']]        
                page_html = BeautifulSoup(page.text, 'html.parser')            
                return page_html
            else:
                horizon[root_url + url] = [True, page.status_code, page.headers['Content-Type']]
                print('The check_url function failed')                
        else:
            horizon[url] = [True, 'bad url', 'bad url']
            logger.info('The checked value of %s is %s' % (url, horizon[url][0]))
            logger.info('All the rules didnt pass')
    else:
        logger.info('We\'ve already checked this link')

def get_links(url):
    current_page_links = {}
    for link in url.find_all('a'):                    
        current_page_links[link.get('href')] = [False, '']
    return current_page_links

def check_for_new_links(current_page_links):
        for url in current_page_links.keys(): 
            if not url in horizon:
                horizon[url] = current_page_links[url]

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
            url[0] != '#',
            url[0:19] == 'http://www.nyrr.org', #Internal link check... And you are checking the same URL over and over...
            url[0:6] != 'mailto'
        ]

    if all(rules):
        return True
    else:
        return False

crawl_website(next(iter(horizon)))