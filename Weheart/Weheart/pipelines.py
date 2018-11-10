# -*- coding: utf-8 -*-
import json
import pymysql


class WeheartPipeline(object):
    def __init__(self):
        self.file = open('weheart.txt', 'w', encoding='utf-8')

    def close_file(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item


class MySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='******',
            db='yyc_admin',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                '''insert into yyc_pinzhanghao_we (user, created_at, imgsaves, url, link)
                values (%s, %s, %s, %s, %s)''',
                (item['user'],
                 item['web_time'],
                 item['hearts'],
                 item['pic_href'],
                 item['link']))
        except:
            self.cursor.execute(
                '''UPDATE yyc_pinzhanghao_we set created_at=%s, imgsaves=%s, link=%s where user=%s and
                url=%s''', (item['web_time'], item['hearts'], item['link'], item['user'], item['pic_href']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
