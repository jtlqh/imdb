# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_id = scrapy.Field()
    review_id = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    username = scrapy.Field()
    date = scrapy.Field()
    rating = scrapy.Field()
    scale = scrapy.Field()
    helpful_votes = scrapy.Field()
    total_votes = scrapy.Field()
