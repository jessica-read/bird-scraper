from bs4 import BeautifulSoup

with open('ScrapeTheBirds/testBirdSite.html', 'r') as html_file:
    content = html_file.read()
    # print(content)

    # soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())

    # bird_name_tags = soup.find_all('h2') #find('h2') will only find the first one, find_all... finds all!
    # print(bird_name_tags)
    
    # for bird in bird_name_tags:
        # print(bird.text)
    
    soup = BeautifulSoup(content, 'lxml')
    bird_reports = soup.find_all('div', class_='report') #have to add underscore to 'class' bc class is a python term
    for report in bird_reports:
        bird_species = report.h2.text
        location = report.find('div', class_='location').text
        state_of_report = report.find('div', class_='location').text.split()[-1] #the split()[-1] gives us the last 'word' of the string

        # print(bird_species)
        # print(location)
        # print(state_of_report)

        print(f'{bird_species} was seen in {state_of_report}, USA!')
