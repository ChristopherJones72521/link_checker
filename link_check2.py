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

# Check only keys with a checked value of false (this is a tough one...)

# Master function (one function to rule them all)
def crawl_website(url):
    if check_url(url):
        new_links = get_links(get_html(url))
        check_for_new_links(new_links)
    else:
        logger.info('You\'ve reached the end of the list! Cheers!')
    # crawl_website(next_link)
    pprint.pprint(horizon)

def check_url(url):
    logger.info('The checked value of %s is %s' % (url, horizon[url][0]))
    if horizon[url][0] == False:
        if  url == root_url:
            logger.info('All rules passed')
            return True
        elif url != None and check_rules(url[20:]):
            logger.info('All rules passed')
            return True
        else:
            horizon[url] = [True, 'bad url', 'bad url']            
            logger.info('All the rules didnt pass')
            return False
    else:
        logger.info('We\'ve already checked this link')
        return False

def get_links(url):
    current_page_links = {}
    
    for link in url.find_all('a'):
        current_page_links[link.get('href')] = [False, '', '']
    return current_page_links

def check_for_new_links(current_page_links):
        for url in current_page_links.keys(): 
            if not url in horizon:
                horizon[root_url + str(url)] = current_page_links[url]

def check_rules(url):
    logger.info('The check_rules function is currently checking %s', url)
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
            url[0:4] != 'http',
            url[0:6] != 'mailto'
        ]
    
    print('The URL %s returned %r to the rule check' % (url, all(rules)))
    if all(rules):
        return True
    else:
        return False

def get_html(url):
    page = requests.get(url)
    if page.status_code == 200 and page.headers['Content-Type'] == 'text/html; charset=utf-8':
        # logger.info('%s is an HTML page and returned a 200', url)
        horizon[url] = [True, page.status_code, page.headers['Content-Type']]        
        page_html = BeautifulSoup(page.text, 'html.parser')            
        return page_html
    else:
        horizon[root_url + url] = [True, page.status_code, page.headers['Content-Type']]
        logger.info('The get_html function failed')      

crawl_website(root_url)