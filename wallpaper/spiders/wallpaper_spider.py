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
        "http://desk.zol.com.cn/meinv/1920x1080/hot_1.html",
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=(r'meinv/1920x1080/hot_\d{,2}.html')), follow=True, callback="parse"),
    ]
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "www.zhihu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
            }
    
    def parse(self, response):
        sel_root = response.xpath('//ul[@class="pic-list2  clearfix"]/li/a/@href')
        for sel in sel_root:
            mv_url = 'http://desk.zol.com.cn' + sel.extract()
            print mv_url
            yield scrapy.Request(mv_url, self.parse_item)

    def parse_item(self,response):
        print 'ddddd'
        sel = response.xpath('//ul[@id="showImg"]/li/a/img/@src').extract() + response.xpath('//ul[@id="showImg"]/li/a/img/@srcs').extract()
        for i in range(len(sel)):
            sel[i] = sel[i].replace("144x90", "1920x1080",1)
        item = WallpaperItem()
        item['imageurl'] = sel
        yield item
