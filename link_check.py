import requests
import validators
import pprint
from logzero import logger
from urllib.parse import urljoin
from bs4 import BeautifulSoup

#TODO Add User Agent data

url = 'https://www.nyrr.org' # This should be the hostname / root URL as we will be appending to it later. 
horizon = [] # All links on the site across all pages. Will be useful for indexing. 
to_visit = [] # links not vistited in the horizon
visited = [] # links already visited. Can be used to reference against to avoid duplicate checking
internal_links = [] # anything without https:// these are the links we will be checking.
external_links = [] # bucket to dump external links. May be useful for reporting
bad_links = [] # anything that does not return a 200
pp = pprint.PrettyPrinter(indent=4)

def crawl_website(root_link):
    tmp_horizon = []
    
    if validators.url(root_link):
        if root_link:
            if check_if_new_link(root_link):            
                #Check to see if this link returns a 200 then set it to a variable
                try:                    
                    page = requests.get(root_link)
                    logger.info(root_link + ' is a new link returning a ' + str(page.status_code))

                    # Add current link to visted links list
                    visited.append(root_link)

                    # If the site returns a success code, then scrape for links
                    if page.status_code == 200 and page.headers['Content-Type'] == 'text/html; charset=utf-8':
                        soup = BeautifulSoup(page.text, 'html.parser')

                        # Find all links
                        for link in soup.find_all('a'):                    
                            tmp_horizon.append(link.get('href'))                    

                        # Scrub list of all irrelevant links
                        for link in tmp_horizon: # there has to be a better way to do the below   
                            try:         
                                if link != None and link != '/' and link != '' and link[0:10] != 'link.aspx?' and link[0:3] != 'tel' and link != '/~' and link != '#' and link[0:10] != 'javascript' and link[0] != '#' and link[0:4] != 'http' and link[0:6] != 'mailto':
                                    # logger.info('The value of link is: ' + link)
                                    full_url = urljoin(url, link) 
                                    # logger.info('The full URL being appended to internal links is: ' + full_url)
                                    internal_links.append(full_url)
                                elif link != None and len(link) > 4 and link[0:4] == 'http':
                                    external_links.append(link)
                            except Exception as e:
                                logger.exception(e)

                        # Check all links in internal links to see if they've been checked before
                        for tmp_link in internal_links:
                            # logger.info('checking: ' + tmp_link)
                            if check_if_new_link(tmp_link):                        
                                # logger.info('Found new link: %s adding to to_visit list', tmp_link)
                                to_visit.append(tmp_link)
                    else:
                        logger.info(root_link + ' is not online ' + '| Status code: ' + str(page.status_code)) # Create a list for pages that are offline. 
                        bad_links.append(root_link + " | Status code: " + str(page.status_code))
                except Exception as e:                    
                    logger.exception('root_link: ' + root_link)
                    pprint.pprint((to_visit))
                    logger.exception(e)
                    bad_links.append(root_link)
                    pass
    #         else:
    #             logger.info('There are no new links to check')
    #     else:
    #         logger.info('There are no links to check')
    # else:
    #     logger.info('Not a valid URL')
    if to_visit:
        crawl_website(to_visit.pop(0))
    else:
        logger.info("These are the bad links found")
        pprint.pprint((bad_links))
        logger.info("You've reached the end of the list. Cheers!")

def check_if_new_link(link_to_check):
    if link_to_check not in to_visit and link_to_check not in visited:
        to_visit.append(link_to_check) # Why is the link added twice?
        return True
    else: 
        return False

crawl_website(url)

#TODO Include website URL as arguments to script
#TODO Create function to visit all links on first page of links and grab links from these pages.
# will have to be a recursive function which automatically visits discovered links and continues until no non-duplicate links exist
#TODO Consider email reporting for failures and possibly a daily link check report (internal and outbound)
#TODO Consider UI Testing (will I need selenium? Or do I just check for the presence of content?)'''