# -*- coding: utf-8 -*-
import scrapy


class WeheartItem(scrapy.Item):
    user = scrapy.Field()
    pic_href = scrapy.Field()
    hearts = scrapy.Field()
    web_time = scrapy.Field()
    link = scrapy.Field()
