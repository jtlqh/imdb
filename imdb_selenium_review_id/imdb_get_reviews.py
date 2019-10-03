from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from db import Review, Movie
from db1 import Reviews, Movies
from dateutil.parser import parse
import re
from time import sleep
import pandas as pd
from datetime import datetime
import sys

def time_mapper(input):
    ''' convert hour to minutes '''
    duration = str(input).strip().split()
    total_minutes = 0
    for x in duration:
        val = re.findall(r'[\d,]+', x)[0]
        key = x.strip(val)
        if key in ['h', 'hours', 'hour', 'hr', 'hrs']:
            total_minutes += int(str(val).replace(',', '')) * 60
        else:
            total_minutes += int(str(val).replace(',', ''))
    return str(total_minutes)



strings = []
with open('imdb.csv', 'r') as f:
    line = f.readline()  # first line is title
    strings = sum([re.findall(r'tt\d+',line) for line in f], [])

strings = list(set(strings))
#completed_t = pd.read_csv('process_title.csv',index_col=0, names=['title_id'], skiprows=[0])
#completed_titles = completed_t['title_id'].tolist()

# query mySQL database for a list of movie titles
finished_titles = [r.title_id for r in Movies.select()]
print("number of records in reviews: ",len(finished_titles))

urls = ['https://www.imdb.com/title/{}/'.format(x) for x in strings]

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\where\you\download\the\chromedriver.exe')

driver = webdriver.Chrome(r'C:\chromedriver.exe')


# extracting movie info
print(len(strings))
for title_id, url in zip(strings, urls):
    #if title_id in completed_titles:
    if title_id in finished_titles:
            continue
    
    print(title_id)
    try:
        driver.get(url)
    except:
        continue        
    item = Movies(
        title_id = title_id
    )
    try:
        item.save()
        
    except:
        continue

#   extracting review ids
    driver.get(url + 'reviews')
    num_of_reviews = re.findall(r'[\d,]+', driver.find_element_by_xpath('//div[@class="header"]/div/span').text)[0]

    print(num_of_reviews)
    num_of_reviews = int(num_of_reviews.replace(',', ''))
    if num_of_reviews <=0:
        continue
  

    while True:
        try:
            wait_event = WebDriverWait(driver, 10)
            button = wait_event.until(EC.element_to_be_clickable((By.ID, "load-more-trigger"))) 
            button.click()
            
        except:
            break

    if num_of_reviews >3000:
        wait_event = WebDriverWait(driver, 60)
    else:
        wait_event = WebDriverWait(driver, 30)

    try:
        elements = wait_event.until(EC.presence_of_all_elements_located((By.XPATH, \
            '//div[@class="lister-list"]/div')))
        print('collected number of reviews ',len(elements))
    except:
        continue
        
    for element in elements:
        review_id = element.get_attribute('data-review-id')
           
        review_item = Reviews(
            title_id = title_id,
            review_id = review_id
                )
        try:
            review_item.save()
        except:
            pass

            
