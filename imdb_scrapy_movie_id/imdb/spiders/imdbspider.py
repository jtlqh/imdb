# -*- coding: utf-8 -*-
import scrapy
from imdb.items import ImdbItem
from scrapy import Request
import re


class ImdbspiderSpider(scrapy.Spider):
    name = 'imdbspider'
    allowed_domains = ['imdb.com']
    start = 1
    start_urls = ['https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,documentary,video_game,short,video,tv_short&release_date=1900-01-01,2019-12-31&start=1&ref_=adv_nxt']


    def check_current_page(self, response):
            text = response.xpath('//div[@class="desc"]/span/text()').extract_first()
            text = text.replace(',','')
            
            start, end, total = [int(num) for num in re.findall('[\d,]+',text)]
            return start, end, total


    def parse(self, response):
            
            
                url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,documentary,video_game,short,video,tv_short&release_date=1900-01-01,2019-12-31&start={}&ref_=adv_nxt'.format(self.start)
 
                yield Request(url=url, callback = self.parse_result_page)
        
    def parse_result_page(self, response):        
            self.start +=50
            titles = response.xpath('//div[@class="lister-list"]/div/div[2]/a/@href').extract()
            titles = [re.findall(r'(tt\d+)',x)[0] for x in titles]
            item = ImdbItem()
            item['title'] = titles
            yield item

            start, end, total = self.check_current_page(response)
            print(self.start, start)
            if self.start <= start + 50:
                
                url = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,documentary,video_game,short,video,tv_short&release_date=1900-01-01,2019-12-31&start={}&ref_=adv_nxt'.format(self.start)
 
                yield Request(url=url, callback = self.parse_result_page)
            else:
                exit(1)
            
        