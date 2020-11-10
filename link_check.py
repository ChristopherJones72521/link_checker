import requests
from bs4 import BeautifulSoup

#TODO Add User Agent data

url = 'https://www.nyrr.org/'
horizon = [] # All links on the site across all pages. Will be useful for indexing. 
to_visit = [] # links not vistited in the horizon
visited = [] # links already visited. Can be used to reference against to avoid duplicate checking
internal_links = [] # anything without https:// these are the links we will be checking.
external_links = [] # bucket to dump external links. May be useful for reporting
bad_links = [] # anything that does not return a 200

def crawl_website(root_link):
    tmp_horizon = []
    # print('Currently checking: %s', root_link)
    
    if root_link:
        if check_if_new_link(root_link):            
            #Check to see if this link returns a 200 then set it to a variable
            page = requests.get(root_link)
            print(root_link + ' is a new link returning a ' + str(page.status_code))
            visited.append(root_link)
            # print('These are the to_visit links: %s ', str(to_visit))
            # print('These are the visited links: %s ', str(visited))
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')

                # Find all links
                for link in soup.find_all('a'):                    
                    tmp_horizon.append(link.get('href'))                    

                # Scrub list of all irrelevant links
                for link in tmp_horizon: # there has to be a better way to do the below
                    if link != None and link != '/' and link != '' and link[0:10] != 'link.aspx?' and link != '~' and link != '#' and link[0:10] != 'javascript' and link[0] != '#' and link[0:4] != 'http' and link[0:6] != 'mailto':
                        internal_links.append('https://www.nyrr.org' + link)
                    elif link != None and len(link) > 4 and link[0:4] == 'http':
                        external_links.append(link)

                # Check all links in internal links to see if they've been checked before
                for tmp_link in internal_links:
                    # print('checking: ' + tmp_link)
                    if check_if_new_link(tmp_link):                        
                        print('Found new link: %s adding to to_visit list', tmp_link)
                        to_visit.append(tmp_link)
            else:
                print('This page is not online') # Create a list for pages that are offline. 
                bad_links.append(root_link)
        else:
            print('There are no new links to check')
    else:
        print('There are no links to check')
    # print(to_visit)
    crawl_website(to_visit.pop(0))

def check_if_new_link(link_to_check):
    # if link_to_check:
    # I need to check if the link exists in either list
    if link_to_check not in to_visit and link_to_check not in visited:
        # print(link_to_check + ' is not in the to_visit list: ' + str(link_to_check not in to_visit))
        # print(link_to_check + ' is not in the visited list: ' + str(link_to_check not in visited))
        to_visit.append(link_to_check)
        return True
    else: 
        return False

crawl_website(url)

#TODO begin checking each page with a console message explaining which page we're gathering or checking links on
#TODO dedup the list of urls
#TODO Include website URL as arguments to script
#TODO Create function to visit all links on first page of links and grab links from these pages.
# will have to be a recursive function which automatically visits discovered links and continues until no non-duplicate links exist
#TODO Check each link against a list of links. If link does not exist in list, add it to the to_visit list
# The approach will be to create the master list of links to check before checking
#TODO Add conditional check for 'is internal' and create separate list 'external_links' for any that don't qualify
#TODO Consider email reporting for failures and possibly a daily link check report (internal and outbound)
#TODO Consider UI Testing (will I need selenium? Or do I just check for the presence of content?)'''