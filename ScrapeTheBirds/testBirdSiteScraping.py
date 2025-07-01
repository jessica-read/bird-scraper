from bs4 import BeautifulSoup

with open('testBirdSite.html', 'r') as html_file:
    content = html_file.read()
    # print(content)

    soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())

    bird_name_tags = soup.find_all('h2') #find('h2') will only find the first one, find_all... finds all!
    # print(bird_name_tags)
    
    for bird in bird_name_tags:
        print(bird.text)
    
    