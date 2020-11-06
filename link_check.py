import requests
from bs4 import BeautifulSoup


url = 'https://www.nyrr.org/'
horizon = [] # All links on the site across all pages. Will be useful for indexing. 
to_visit = [] # links not vistited in the horizon
visited = [] # links already visited. Can be used to reference against to avoid duplicate checking
internal_links = [] # anything without https:// these are the links we will be checking.
external_links = [] # bucket to dump external links. May be useful for reporting

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

# Find all links
for link in soup.find_all('a'): # Should I pop each link found into this list?
    horizon.append(link.get('href'))

# clean up data in this list (ex. '/', '', '#', 'javascript:;', begins with '#', begins with 'http')
# iterage through the horizon list and move internal links to the internal link list
for link in horizon:
    if link != None and link != '/' and link != '' and link != '#' and link[0:10] != 'javascript' and link[0] != '#' and link[0:4] != 'http' and link[0:6] != 'mailto':
        internal_links.append(link)
    elif link != None and len(link) > 4 and link[0:4] == 'http':
        external_links.append(link)

for link in internal_links:
    print(link) 


# Create function to check all links on first page for status 200
# for link in horizon: 
#   link.status_code # if status code != 200 then store this link in a list

# Create function to visit all links on first page of links and grab links from these pages
# will have to be a recursive function which automatically visits discovered links and continues until no non-duplicate links exist
# Check each link against a list of links. If link does not exist in list, add it to the to_visit list
# Add conditional check for 'is internal' and create separate list 'external_links' for any that don't qualify

