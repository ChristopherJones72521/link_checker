import pprint
pp = pprint.PrettyPrinter(indent=4)

# Challenge #1 create fake dict and compare links in a list to it?
horizon = {
    'https://www.nyrr.org' : [False, 200],
    'https://www.nyrr.org/About' : [False, 200],
    'https://www.nyrr.org/About/Our-Programs' : [False, 200],
    'https://www.nyrr.org/About/Partners' : [False, 200],
    'https://www.nyrr.org/About/Our-Team' : [False, 200],
    'https://www.nyrr.org/About/Mission-and-Impact' : [False, 200],
    'https://www.nyrr.org/About/Our-Core-Values' : [False, 200],
    'https://www.nyrr.org/About/Careers' : [False, 200],
    'https://www.nyrr.org/About/History' : [False, 200],
    'https://www.nyrr.org/tcsnycmarathon' : [False, 200],
    'https://www.nyrr.org/RunCenter' : [False, 200],
    'https://www.nyrr.org/media-center' : [False, 200],
    'https://www.nyrr.org/Community' : [False, 200],
    'https://www.nyrr.org/GetInvolved/Donate' : [False, 200],
    'https://www.nyrr.org/Gift-Card?productId=20001' : [False, 200],
    'https://www.nyrr.org/join' : [False, 200],
    'https://www.nyrr.org/run/race-calendar' : [False, 200],
    'https://www.nyrr.org/Run/Photos-And-Stories' : [False, 200],
    'https://www.nyrr.org/Run/Virtual-Racing' : [False, 200],
    'https://www.nyrr.org/Run/Striders' : [False, 200],
    'https://www.nyrr.org/OpenRun' : [False, 200],
    'https://www.nyrr.org/Run/Run-With-Charity' : [False, 200],
    'https://www.nyrr.org/Run/Race-Free' : [False, 200]
}

current_page_links = {
    'https://www.nyrr.org' : [False, ''],
    'https://www.nyrr.org/About' : [False, ''],
    'https://www.nyrr.org/About/Our-Programs' : [False, ''],
    'https://www.nyrr.org/About/Partners' : [False, ''],
    'https://www.nyrr.org/About/Our-Team' : [False, ''],
    'https://www.nyrr.org/Run/Guidelines-and-Procedures' : [False, ''],
    'https://www.nyrr.org/Run/Five-Borough-Series' : [False, ''],
    'https://www.nyrr.org/Run/Guaranteed-Entry' : [False, ''],
    'https://www.nyrr.org/Run/International-Runners' : [False, ''],
    'https://www.nyrr.org/Youth' : [False, ''],
    'https://www.nyrr.org/Youth/AboutRisingNYRR' : [False, ''],
    'https://www.nyrr.org/Youth/Races-And-Events' : [False, ''],
    'https://www.nyrr.org/Youth/FAQ' : [False, ''],
    'https://www.nyrr.org/Youth/Photos-and-Stories' : [False, ''],
    'https://www.nyrr.org/Youth/20-Years' : [False, ''],
    'https://www.nyrr.org/Train' : [False, ''],
    'https://www.nyrr.org/Train/Classes/CoachingLab' : [False, ''],
    'https://www.nyrr.org/Train/Classes/OutdoorRunningClass' : [False, '']
}

# Grab URL from dict
# Check if HTML page and what the status code is
# Update this link's status code
# Update that link's bool to True
# Pull all links from web page
# Assign links as keys to new dict
# Compare all keys from new dict to horizon, if new add to horizon
for url in current_page_links.keys(): 
    if not url in horizon:
        horizon[url] = current_page_links[url] # you could even do this with a list


# Repeat for the next link
# At the end of this process, print horizon
# pprint.pprint(horizon)
res = next(iter(horizon))
print(res)

# Challenge #2 pull all links off of website and store as dict keys, the values will be [has_been_checked, status code, ]