# Eivind Norling - INFO215 - Oblig03


import re
import time
import random
import networkx as nx
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def init():
    # Launch options and driver init
    chrome_options = Options()
    chrome_options.add_argument("--kiosk")
    driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)

    G = nx.Graph()

    hashtags = str(input('Type in hashtags to search:'))
    tags = hashtags.split(',')

    for tag in tags:
        crawl(G, tag, driver)

    print(list(G.nodes))

    tags = nx.get_node_attributes(G, 'tag')
    print('London:', list(tags.values()))
    print(G.nodes.data())

    for tag in tags.items():
        print(tag)

    input('Press ENTER to close the     automated browser')
    driver.quit()


def crawl(graph, tag, driver):
    # Initializes URL and tells webdriver to open that URL
    url = 'https://twitter.com/search?q=%23' + tag
    driver.get(url)

    # Keeps track of tags visited
    tag_count = 0
    used_tags = []
    first_run = True

    if first_run:
        hashtag = str('#' + tag)
        used_tags.append(hashtag)
        graph.add_node(hashtag, tag=hashtag)

    graph.graph['tag'] = tag

    while tag_count < 3:

        # wait for website to load
        time.sleep(5)

        # init BS parser with page HTML source
        bs = BeautifulSoup(driver.page_source, 'html.parser')

        # creates a list to store all a tags with href that starts with '/hashtag/'
        tag_list = []

        count = 0

        # appends all found hashtags objects to that list
        for found_tags in bs.find_all('a', href=re.compile('/hashtag/?')):
            if not first_run:
                count += 1
                if count > 5:
                    print('Found ::', found_tags['href'])
                    tag_list.append(str(found_tags.text))
            else:
                first_run = False
                print('Found ::', found_tags['href'])
                tag_list.append(str(found_tags.text))

        # choose a random tag from list
        chosen_tag = str(random.choice(tag_list))

        if used_tags.__contains__(chosen_tag):
            tag_list.remove(chosen_tag)
            chosen_tag = random.choice(tag_list)

        used_tags.append(str(chosen_tag))
        print('Chosen tag ::', chosen_tag)

        graph.add_node(chosen_tag, tag=tag)

        # finds the first element with that specific link.text object
        link = driver.find_element_by_link_text(chosen_tag)

        # Executes some JS to scroll that element into view if needed
        driver.execute_script("arguments[0].scrollIntoViewIfNeeded({block: 'start'});", link)
        # Scroll a bit up cause scrollIntoView scrolls way to far on twitter for some weird reason
        ActionChains(driver).move_by_offset(0, 100).perform()

        # wait to ensure object has time to load in
        time.sleep(3)

        # click that link
        link.click()

        # increment counter and start loop again if visited less then 6 links
        tag_count += 1

    print(used_tags)
    used_tags.clear()


if __name__ == '__main__':
    init()
