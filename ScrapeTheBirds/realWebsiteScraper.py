from bs4 import BeautifulSoup
import requests

def parse_bird_sightings(notts_birders_content):
    bird_soup = BeautifulSoup(notts_birders_content, 'lxml')
    sightings = []

    # iterates through h2 tags holding the dates
    for h2 in bird_soup.find_all('h2', class_='main_content_title'):
        date = h2.get_text(strip=True)
        current = h2.find_next_sibling()

        # while the next line is not h2
        while current and not (current.name == 'h2' and 'main_content_title' in current.get('class', [])):
            if current.name == 'p':
                # Identify location from span.style19 > strong
                location = None
                location_span = current.find('span', class_='style19')
                if location_span:
                    strong_in_span = location_span.find('strong')
                    if strong_in_span:
                        location = strong_in_span.text.strip()

                if not location:
                    current = current.find_next_sibling()
                    continue

                bird_entries = []

                for element in current.find_all(['span', 'strong']):
                    # Skip the location strong tag
                    if element.name == 'strong' and element in location_span.find_all('strong'):
                        continue

                    bird_name = element.get_text(strip=True)

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

                    bird_entries.append({'name': bird_name, 'rarity': rarity})

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
    print(organised_data)
else:
    print("Failed to retrieve page:", response.status_code)