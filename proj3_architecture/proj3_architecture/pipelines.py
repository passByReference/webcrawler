# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# To use pipeline, need to modify settings.py
class Proj3ArchitecturePipeline(object):
    def process_item(self, item, spider):
        if item['_h1_tag']:
            item['_h1_tag'] = item['_h1_tag'][0].upper()
        return item
