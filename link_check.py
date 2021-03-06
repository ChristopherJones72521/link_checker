import requests
import validators
import pprint
from logzero import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup

url = 'https://www.nyrr.org' # This should be the hostname / root URL as we will be appending to it later.  
to_visit = [] # links not vistited in the horizon
visited = [] # links already visited. Can be used to reference against to avoid duplicate checking
internal_links = [] # anything without https:// these are the links we will be checking.
external_links = [] # bucket to dump external links. May be useful for reporting
bad_links = [] # anything that does not return a 200
pp = pprint.PrettyPrinter(indent=4)

def crawl_website(root_link):
    tmp_horizon = []

    try:
        if check_if_new_link(root_link):

            # Assign webpage to page object
            try:
                page = requests.get(root_link) #The issue is somehow here?
                # If the site returns a success code, then scrape for links        
                if page.status_code == 200 and page.headers['Content-Type'] == 'text/html; charset=utf-8':
                    logger.info('%s is an HTML page and returned a 200', root_link)
                    soup = BeautifulSoup(page.text, 'html.parser')

                    # Find all links
                    for link in soup.find_all('a'):                    
                        tmp_horizon.append(link.get('href'))                    

                    # Scrub list of all irrelevant links
                    clean_links(tmp_horizon)

                    # Check all links in internal links to see if they've been checked before
                    for tmp_link in internal_links:
                        if check_if_new_link(tmp_link):                        
                            to_visit.append(tmp_link)
                else:                
                    logger.info(root_link + ' is not returning a 200 or is not an HTML page ' + '| Status code: ' + str(page.status_code))
                    bad_links.append(root_link + " | Status code: " + str(page.status_code))

            except Exception as e:
                logger.exception('There was an error checking root_link, %s : %s' % (root_link, e))
                pass

            # Add current link to visted links list            
            visited.append(root_link)        

        check_next_link(to_visit)
        
    except Exception as e:                    
        logger.exception('root_link: ' + root_link)
        logger.exception(e)
        bad_links.append(root_link)
        pprint.pprint((bad_links))

def check_next_link(links_to_visit):
    if links_to_visit: # If the to_visit list contains a value
        latest_link = to_visit.pop(0)
        try: 
            if validators.url(latest_link) and latest_link:
                logger.info('Now checking: %s', latest_link)
                crawl_website(latest_link)
            else:
                logger.info('%s is not a valid URL', latest_link)
                logger.info(latest_link)
                bad_links.append(latest_link)
                the_next_next_link = links_to_visit.pop(0)
                check_next_link(the_next_next_link)
        except Exception as e:
            logger.info(latest_link)
            logger.exception(e)
    else:
        logger.info("These are the bad links found")
        pprint.pprint((bad_links))
        logger.info("You've reached the end of the list. Cheers!")

def check_if_new_link(link_to_check):
    if link_to_check not in to_visit and link_to_check not in visited:        
        return True
    else: 
        return False

def clean_links(list_of_links):
    # Scrub list of all irrelevant links
    for link in list_of_links:
        # if link != None and link != '' and link != '/':
        #     logger.info('Link %s link[0:10] != \'javascript\': %r' % (link, link[0:10] != 'javascript'))
        try:         
            if link != None and link != '/' and link != '' and link[0:10] != 'link.aspx?' and link[0:3] != 'tel' and link != '/~' and link != '#' and link[0:10] != 'javascript' and link[0] != '#' and link[0:4] != 'http' and link[0:6] != 'mailto':                
                full_url = urljoin(url, link) 
                internal_links.append(full_url)                
            elif link != None and len(link) > 4 and link[0:4] == 'http':
                external_links.append(link)
        except Exception as e:
            logger.exception(e)

crawl_website(url)

#TODO Verbose mode
#TODO Add User Agent data
#TODO Include website URL as argument
#TODO Consider email reporting for failures and possibly a daily link check report (internal and outbound)
#TODO MS Teams integration?
#TODO Consider UI Testing (will I need selenium? Or do I just check for the presence of content?)'''