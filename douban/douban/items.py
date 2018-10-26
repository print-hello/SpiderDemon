'''
Author: Vinter Wang
'''
# -*- coding: utf-8 -*-
import scrapy


class DoubanItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    grade = scrapy.Field()
    tags = scrapy.Field()
    link = scrapy.Field()
    playable = scrapy.Field()
