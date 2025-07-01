from bs4 import BeautifulSoup
import requests

def parse_bird_sightings(notts_birders_content):
    # print(f'Oh dear... here we go: \n {notts_birders_content}')
    bird_soup = BeautifulSoup(notts_birders_content, 'lxml') #parses the entire website through BS
    bird_species = bird_soup.find('span', class_ = 'style6')

    print(bird_species) #JESS!!! SO FAR IT FINDS THE FIRST STLYE6 SPAN, NOT QUITE WHAT I WANTED BUT WE MOVE
    returning_data = bird_species
    return returning_data

# <p><span class="style19"><strong>Holme Pierrepont</strong></span> -	
#   <span class="style6">Cattle Egret</span> [circled Blotts Pit and flew west, 18:17]; also <span class="style6">Common Sandpiper</span>. 
# </p>

# Fetch HTML from the website
url = "https://www.nottsbirders.net/latest_sightings.html"
response = requests.get(url)

if response.status_code == 200:
    notts_birders_content = response.text #content from the notts birders website
    organised_data = parse_bird_sightings(notts_birders_content)
    # print(organised_data)
else:
    print("Failed to retrieve page:", response.status_code)