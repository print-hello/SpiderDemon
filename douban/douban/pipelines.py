# -*- coding: utf-8 -*-
import json
import pymysql


class DoubanPipeline(object):
    def __init__(self):
        self.file = open('doubanTOP250.txt', 'w', encoding='utf-8')

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
            password='123456',
            db='spiderinfo',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                '''insert into doubanmovie(rank, title, score, tags, link, playable)
                values (%s, %s, %s, %s, %s, %s)''',
                (item['rank'],
                 item['title'],
                 item['score'],
                 item['tags'],
                 item['link'],
                 item['playable']))
            self.conn.commit()
        except:
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
