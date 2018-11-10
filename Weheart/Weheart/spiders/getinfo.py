# -*- coding: utf-8 -*-
import scrapy
from Weheart.items import WeheartItem
import datetime
import pymysql


class GetinfoSpider(scrapy.Spider):
    name = 'getinfo'
    allowed_domains = ['weheartit.com']

    def start_requests(self):
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='******',
            db='yyc_admin',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        sql = "SELECT user from yyc_domain_to_user_we"
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        conn.close()
        user_in_sql_list = []
        for res in results:
            if res:
                user_in_sql = res['user'].split('/')[-1]
                user_in_sql_list.append(user_in_sql)
        for start_urls_part in user_in_sql_list:
            yield scrapy.Request('https://weheartit.com/'+start_urls_part+'?page=1',
                                  meta={'user': start_urls_part},
                                  callback=self.parse)

    def parse(self, response):
        for href in response.css('div.no-padding>div>a::attr(href)'):
            start_urls_part = response.meta['user']
            pic_url_part = href.extract()
            pic_url = 'https://weheartit.com'+pic_url_part
            yield scrapy.Request(pic_url, meta={'user': start_urls_part}, callback=self.parse_item)

    def parse_item(self, response):
        item = WeheartItem()
        item['user'] = response.meta['user']
        try:
            pic_href = response.css('div.grid>div>div>div>a::attr(href)').extract()
            item['pic_href'] = pic_href[0]
        except:
            item['pic_href'] = response.xpath('//link[@rel="canonical"]/@href')[0].extract()
        web_time = response.css('abbr.timeago::attr(title)').extract()
        if web_time:
            item['web_time'] = web_time[0].replace('T', ' ').replace('Z', '').strip()
        else:
            item['web_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            hearts = response.css('div.text-small a.text-strong>span::text').extract()
            item['hearts'] = hearts[0]
        except:
            item['hearts'] = response.xpath('//span[@class="js-heart-count"]/text()')[0].extract()
        link = response.xpath('//p/a[@class="text-strong text-primary"]/@href').extract()
        if link:
            item['link'] = link[0]
        else:
            item['link'] = ' '
        yield item




