# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy.selector 

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    start_urls = (
        'http://www.google.com/',
    )

    def parse(self, response):
        hxs = scrapy.selector(response)
        sites = hxs.select('//title/text()')
        for site in sites:
            print site.extract()
