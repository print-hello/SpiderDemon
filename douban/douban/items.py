# -*- coding: utf-8 -*-
import scrapy


class DoubanItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    score = scrapy.Field()
    tags = scrapy.Field()
    link = scrapy.Field()
    playable = scrapy.Field()
