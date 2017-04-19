# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinacrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    report_url = scrapy.Field()
    report_title = scrapy.Field()
    report_time = scrapy.Field()
    report_content = scrapy.Field()
