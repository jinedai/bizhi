# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
import json
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('wallpaper.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        for image_url in item['imageurl']:
            yield Request(image_url)

    def item_completed(self,results,item,info):
    	image_paths=[x['path'] for ok,x in results if ok]
    	if not image_paths:
    		raise DropItem('�Ҳ���ͼƬ %s'%image_paths)
        item['imageurl'] = image_paths
        return item

