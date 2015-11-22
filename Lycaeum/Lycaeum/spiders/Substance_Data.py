# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from Lycaeum.items import LycaeumItem 

class SubstanceDataSpider(CrawlSpider):
    name = "Substance_Data"
    allowed_domains = ["www.lycaeum.org"]
    start_urls = ['http://www.lycaeum.org/wiki/Main_Page']
         
    rules = [
    Rule(LinkExtractor(allow=r'/wiki/.+'), callback='parse_item', follow=True)
]
    
    def parse_item(self, response):
        Substance_data = LycaeumItem()
        h1selectors = response.css('h1')
        for h1 in h1selectors:
            Substance_data["Substance"] = h1.xpath('//h1[@class="firstHeading"]/span//text()').extract()
        textselectors = response.css('body')
        for text in textselectors:
            Substance_data["Text"] = ''.join(text.select('//body//div[@class = "mw-content-ltr"]//text()').extract()).strip()
        Substance_data["Substance"] = str(Substance_data["Substance"])[3:-2].strip()
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('\\' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('?' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('*' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('"' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('|' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('>' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('<' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace('/' , "")
        Substance_data["Substance"] = str(Substance_data["Substance"]).replace(':' , "")
        
            
            
        
        yield Substance_data
        