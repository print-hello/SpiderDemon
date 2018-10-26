# -*- coding: utf-8 -*-
import json


class DoubanPipeline(object):
    def __init__(self):
        self.file = open('doubanTOP250', 'w', encoding='utf-8')

    def close_file(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
