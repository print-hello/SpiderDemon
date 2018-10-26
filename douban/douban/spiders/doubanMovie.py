'''
Author: Vinter Wang
'''
# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/top250']

    def parse(self, response):
        items = []
        for info in response.css('div.item'):
            item = DoubanItem()
            item['id'] = info.css('div.pic>em::text').extract()
            # item['title'] = info.css('div.pic a>img::attr(alt)').extract()
            item['title'] = info.xpath('div[@class="pic"]/a/img/@alt').extract()
            item['grade'] = info.css('div.pic>em::text').extract()
            item['tags'] = info.css('span.inq::text').extract()
            item['link'] = info.css('div.hd>a::attr(href)').extract()
            item['playable'] = info.css('span.playable::text').extract()
            items.append(item)
            yield  item

        next_page = response.css('span.next a::attr(href)')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse, allow_redirects=False)


