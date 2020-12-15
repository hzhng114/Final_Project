from bs4 import BeautifulSoup
import requests
import json
import time
import sqlite3
import json
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

cookies = {'birthtime': '568022401'}

def load_cache(CACHE_FILE_NAME):
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache_dict, CACHE_FILE_NAME):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache_dict)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache):
    if (url in cache.keys()):
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        response = requests.get(url, cookies = cookies)
        cache[url] = response.text 
        save_cache(cache, CACHE_FILE_NAME)
        return cache[url]

CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = load_cache(CACHE_FILE_NAME)

class GameDetail:
    def __init__(self, url, rank, name, release_date, percentage_review, num_reviews, price):
        self.url = url
        self.rank = rank
        self.name = name
        self.release_date = release_date
        self.percentage_review = percentage_review
        self.num_reviews = num_reviews
        self.price = price


def build_game_list():
    global game_url_list
    game_tuple_list = []
    game_instance_list = []
    game_url_list = []
    browser = webdriver.Chrome()
    browser.get("https://store.steampowered.com/search/?category1=998&os=win")
    time.sleep(1)
    parent = browser.find_element_by_tag_name("body")
    no_of_pagedowns = 20

    while no_of_pagedowns:
        parent.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1

    info = browser.find_element_by_id('search_resultsRows')
    index = 1
    top_300_games = info.find_elements_by_tag_name('a')
    for games in top_300_games:
        games_rank = index
        index += 1

        games_url = games.get_attribute('href')

        games_name_element = games.find_element_by_class_name('title')
        games_name = games_name_element.text

        games_release_date_element = games.find_element_by_class_name('col.search_released.responsive_secondrow')
        games_release_date = games_release_date_element.text

        games_all_reviews_element = games.find_element_by_class_name('col.search_reviewscore.responsive_secondrow')
        try:
            games_all_reviews_span = games_all_reviews_element.find_element_by_tag_name('span')
        except:
            games_all_reviews_span = "N/A"
        try:
            games_all_reviews_raw = games_all_reviews_span.get_attribute('data-tooltip-html')
            games_percentage_review = int(re.findall('\d*%', games_all_reviews_raw)[0].replace('%', ""))
            games_num_reviews = int(games_all_reviews_raw.split('the', 1)[1].split(" ", 2)[1].replace(",", ""))
        except:
            games_percentage_review = "N/A"
            games_num_reviews = "N/A"

        try:
            games_price_element = games.find_element_by_class_name('col.search_price.discounted.responsive_secondrow')
        except NoSuchElementException:
            games_price_element = games.find_element_by_class_name('col.search_price.responsive_secondrow')
        except:
            games_price_element = 'N/A'
        games_price = games_price_element.text.strip()
        if "Free" in games_price:
            games_price = 0
        elif games_price == "":
            games_price = 0
        elif '\n' in games_price:
            games_price = games_price.split('\n')[1].replace("$", "")
        else:
            games_price = games_price.replace("$", "")
        
        game_instance = GameDetail(games_url, games_rank, games_name, games_release_date, games_percentage_review, games_num_reviews, games_price)
        game_instance_list.append(game_instance)
        game_url_list.append(games_url)
    
    for games in game_instance_list:
        game_tuple = (games.rank, games.name, games.price, games.release_date, games.percentage_review, games.num_reviews, games.url)
        game_tuple_list.append(game_tuple)
    
    return game_tuple_list
    browser.quit()

def save_game_tuple_sqlite(game_tuple_list):
    conn = sqlite3.connect('game_list.db')
    c = conn.cursor()
    return None

def create_games_database(tuple_list):
    conn = sqlite3.connect('Steam_Top_300_Games.sqlite')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS "Games"''')
    query = '''
        CREATE TABLE IF NOT EXISTS "Games"(
        Rank integer PRIMARY KEY AUTOINCREMENT UNIQUE,
        Name text,
        Price float, 
        ReleaseDate text,
        PercentageReview integer,
        NumberofReviews integer,
        URL text)
    '''
    c.execute(query)
    
    c.executemany('INSERT INTO Games VALUES(?,?,?,?,?,?,?)', tuple_list)
    conn.commit()
    conn.close
    return None



def build_game_details_list(game_url_list):
    game_details_tuple_list = []
    for url in game_url_list:
        response = make_url_request_using_cache(url, CACHE_DICT)
        soup = BeautifulSoup(response, 'html.parser')
        site_details_parent = soup.find('div', class_='details_block')

        try:
            genre_parent = site_details_parent.find_all('a', recursive=False)
            genre = str(genre_parent[0].get_text().strip())
        except:
            genre = 'N/A'
    
        try:
            title_tag = site_details_parent.find('b', text='Title:')
            title = title_tag.next_sibling.strip()
        except:
            title = 'N/A'

        try:
            more_detail = site_details_parent.find_all('div', class_='dev_row')
            Developer = more_detail[0].find('a').get_text().strip()
        except:
            Developer = 'N/A'
        try:
            more_detail = site_details_parent.find_all('div', class_='dev_row')
            Publisher = more_detail[1].find('a').get_text().strip()
        except:
            Publisher = 'N/A'
        try:
            more_detail = site_details_parent.find_all('div', class_='dev_row')
            Franchise = more_detail[2].find('a').get_text().strip()
        except:
            Franchise = 'N/A'
        
        game_details_tuple = (title, genre, Developer, Publisher, Franchise)
        game_details_tuple_list.append(game_details_tuple)
    
    return game_details_tuple_list

def save_game_details_tuple_sqlite(game_details_tuple_list):
    conn = sqlite3.connect('game_details_list.db')
    c = conn.cursor()
    return None

def create_games_details_database(tuple_list):
    conn = sqlite3.connect('Steam_Top_300_Games.sqlite')
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS "Games_Details"''')
    query = '''
        CREATE TABLE IF NOT EXISTS "Games_Details"(
        Name text PRIMARY KEY,
        Main_Genre text, 
        Developer text,
        Publisher integer,
        Franchise text)
    '''
    c.execute(query)
    
    c.executemany('INSERT OR IGNORE INTO Games_Details VALUES(?,?,?,?,?)', tuple_list)
    conn.commit()
    conn.close
    return None


if __name__ == "__main__":
    Game_Tuple = build_game_list()
    Game_Details_Tuple = build_game_details_list(game_url_list)
    create_games_database(Game_Tuple)
    create_games_details_database(Game_Details_Tuple)
