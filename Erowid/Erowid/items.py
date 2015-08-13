# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErowidItem(scrapy.Item):
    Title = scrapy.Field()
    Author = scrapy.Field()
    Text = scrapy.Field()
    substance = scrapy.Field()
    # name = scrapy.Field()
