# -*- coding: utf-8 -*-
import scrapy
from imdb_review.items import ImdbReviewItem
from scrapy import Request

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from imdb_reviews.spiders.db1 import Reviews
from imdb_review.db1 import Reviews
import time

class ImdbreviewSpider(scrapy.Spider):
    name = 'imdbreview'
    allowed_domains = ['imdb.com']
    start_urls = ['http://imdb.com/']

    def parse(self, response):
            name = 'imdb_review'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com']
    #for url in start_urls:
    #    yield Request(url=url, callback = self.parse_page)

    def parse(self, response):
        
        
        
        for x in Reviews.select().where(Reviews.summary.is_null()):
            meta = {
                'title_id' : x.title_id,
                'review_id' : x.review_id
                }
            url = 'https://www.imdb.com/review/{}'.format(x.review_id)
        
            yield Request(url=url, meta = meta, callback = self.parse_result)

    def parse_result(self, response):
        item = ImdbReviewItem()
        item['title_id'] = response.meta['title_id']
        item['review_id'] = response.meta['review_id']
        
        #Do some XPath selection with Scrapy
        try:
            item['rating'] = response.xpath('//span[@class="rating-other-user-rating"]/span[1]/text()').extract_first()
        except:
            pass

        item['scale'] = 10
        item['summary'] = response.xpath('//div[@class="lister-item-content"]/a/text()').extract_first()
        try:
            item['content'] = ' '.join(response.xpath('//div[@class="content"]/div[1]/text()').extract())
        
        except:
            
            
            sel = webdriver.Chrome(r'C:\chromedriver.exe')

            sel.set_page_load_timeout(120)
            
            sel.get(response.url)
            time.sleep(2.5)
     
            #Wait for javscript to load in Selenium
            
            wait_event = WebDriverWait(sel, 10)
            #Do some crawling of javascript created content with Selenium
            expander_button = wait_event.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="expander-icon-wrapper spoiler-warning__control"]')))
            expander_button.click()
            item['content'] = sel.find_element_by_xpath('//div[@class="content"]/div[1]').text
        
        voting_string = response.xpath('//div[@class="actions text-muted"]/text()').extract_first()
        voting_string = re.findall(r'[\d,]+', voting_string)
        item['helpful_votes'], item['total_votes']  = [x.replace(',', '') for x in voting_string]
        
        
        item['date'] = response.xpath('.//span[@class="review-date"]/text()').extract_first()
        #date = parse(date)
        
        item['username'] = response.xpath('.//div[@class="parent"]/h3/a/text()').extract_first()
        
        yield item

