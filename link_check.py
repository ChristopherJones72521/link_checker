import requests
from bs4 import BeautifulSoup


url = 'https://www.nyrr.org/'
horizon = [] # All links on the site across all pages. Will be useful for indexing. 
to_visit = [] # links not vistited in the horizon
visited = [] # links already visited. Can be used to reference against to avoid duplicate checking
internal_links = [] # anything without https:// these are the links we will be checking.
external_links = [] # bucket to dump external links. May be useful for reporting
bad_links = [] # anything that does not return a 200

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

# Find all links
for link in soup.find_all('a'):
    horizon.append(link.get('href'))

# Scrub list of all irrelevant links
for link in horizon: # there has to be a better way to do the below
    if link != None and link != '/' and link != '' and link != '#' and link[0:10] != 'javascript' and link[0] != '#' and link[0:4] != 'http' and link[0:6] != 'mailto':
        internal_links.append(link)
    elif link != None and len(link) > 4 and link[0:4] == 'http':
        external_links.append(link)

#TODO begin checking each page with a console message explaining which page we're gathering or checking links on
#TODO dedup the list of urls 

for link in internal_links:
    full_url = 'https://www.nyrr.org' + link
    page = requests.get(full_url)
    print('Status: ' + str(page.status_code) + ' | ' + link)
    # if full_url.status_code != '200':
    #     bad_links.append(link)

# for link in bad_links: 
#     print(bad_links)

#TODO Include website URL as arguments to script
#TODO Create function to visit all links on first page of links and grab links from these pages.
# will have to be a recursive function which automatically visits discovered links and continues until no non-duplicate links exist

#TODO Check each link against a list of links. If link does not exist in list, add it to the to_visit list
# The approach will be to create the master list of links to check before checking

#TODO Add conditional check for 'is internal' and create separate list 'external_links' for any that don't qualify