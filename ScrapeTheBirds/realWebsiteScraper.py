from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint

def parse_bird_sightings(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    sightings = []

    for h2 in soup.find_all('h2', class_='main_content_title'):
        date = h2.get_text(strip=True)
        current = h2.find_next_sibling()

        while current and not (current.name == 'h2' and 'main_content_title' in current.get('class', [])):
            if current.name == 'p':
                # Get location from <span class="style19"><strong>
                location = None
                location_span = current.find('span', class_='style19')
                location_tag = None

                if location_span:
                    strong_in_span = location_span.find('strong')
                    if strong_in_span:
                        location = strong_in_span.text.strip()
                        location_tag = strong_in_span

                if not location:
                    current = current.find_next_sibling()
                    continue

                bird_entries = []
                last_number = None

                for element in current.contents:
                    # Track counts that are strings with numbers
                    if isinstance(element, str):
                        numbers = re.findall(r'\b\d+\b', element)
                        last_number = int(numbers[0]) if numbers else None
                        continue

                    # Skip the <strong> that is part of the location
                    if element == location_tag:
                        continue

                    # Only process span and strong tags
                    if element.name in ['span', 'strong']:
                        bird_name = element.get_text(strip=True).title()

                        if element.name == 'strong':
                            rarity = 'unconfirmed'
                        elif 'style6' in element.get('class', []):
                            rarity = 'interesting'
                        elif 'style47' in element.get('class', []):
                            rarity = 'rare'
                        elif 'style96' in element.get('class', []):
                            rarity = 'very rare'
                        else:
                            continue

                        bird_entries.append({
                            'species': bird_name,
                            'count': last_number if last_number is not None else 'No count specified',
                            'rarity': rarity
                        })

                        last_number = None  # Reset after using it

                if bird_entries:
                    sightings.append({
                        'date': date,
                        'location': location,
                        'birds': bird_entries
                    })

            current = current.find_next_sibling()

    return sightings





# Fetch HTML from the website
url = "https://www.nottsbirders.net/latest_sightings.html"
response = requests.get(url)

if response.status_code == 200:
    notts_birders_content = response.text #content from the notts birders website
    organised_data = parse_bird_sightings(notts_birders_content)
    pprint(organised_data)
else:
    print("Failed to retrieve page:", response.status_code)