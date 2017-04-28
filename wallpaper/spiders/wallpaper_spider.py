#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule 
from scrapy.selector import Selector
from wallpaper.items import WallpaperItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spider import Spider

class WallpaperSpider(CrawlSpider) : #CrawlSpider用来遍布抓取，通过rules来查找所有符合的URL来爬取信息
    name = "wallpaper"
    allowed_domains = ["zol.com.cn"]
    start_urls = [
        "http://desk.zol.com.cn/bizhi/265_1288_2.html",
    ]
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "www.zhihu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
            }
    
    def parse(self,response):
        item = WallpaperItem()
        sel = response.xpath('//ul[@id="showImg"]/li/a/img/@src').extract() + response.xpath('//ul[@id="showImg"]/li/a/img/@srcs').extract()
        for i in range(len(sel)):
            item['imageurl'][i] = sel[i].replace("144x90", "1920x1080",1)
        yield item
