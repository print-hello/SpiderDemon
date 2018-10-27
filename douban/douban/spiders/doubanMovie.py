'''
Author: Vinter Wang
Email: printhello@163.com
'''
# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        items = []
        for info in response.css('div.item'):
            item = DoubanItem()
            item['rank'] = info.css('div.pic>em::text')[0].extract()
            item['title'] = info.css('div.pic a>img::attr(alt)')[0].extract()
            item['score'] = info.css('span.rating_num::text')[0].extract()
            item['tags'] = info.css('span.inq::text')[0].extract()
            item['link'] = info.css('div.hd>a::attr(href)')[0].extract()
            playable = info.css('span.playable::text').extract()
            if playable:
                playable = playable[0]
            else:
                playable = '[无播放源]'
            item['playable'] = playable
            items.append(item)
            yield  item

        next_page = response.css('span.next a::attr(href)')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)


