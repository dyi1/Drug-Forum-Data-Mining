# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from Lycaeum.items import LycaeumItem 

forum_numbers = [2,3,28,14,36,16,6]

class ForumcrawlerSpider(CrawlSpider):
    name = "forumCrawler"
    allowed_domains = ["www.lycaeum.org"]
    start_urls = ['http://www.lycaeum.org/forum/index.php?board=%.01f'%float(forum_number) 
                    for forum_number in forum_numbers]
         
    rules = [
    Rule(LinkExtractor(allow=r'/forum/index.php/board,2.[\d]+.html'), follow=True),
    Rule(LinkExtractor(allow=r'/forum/index.php/board,3.[\d]+.html'), follow=True),
    Rule(LinkExtractor(allow=r'/forum/index.php/board,28.[\d]+.html'), follow=True),
    Rule(LinkExtractor(allow=r'/forum/index.php/board,14.[\d]+.html'), follow=True),
    Rule(LinkExtractor(allow=r'/forum/index.php/board,36.[\d]+.html'), follow=True),
    Rule(LinkExtractor(allow=r'/forum/index.php/board,16.[\d]+.html'), follow=True),
    Rule(LinkExtractor(allow=r'/forum/index.php/board,6.[\d]+.html'), follow=True),
    Rule(LinkExtractor(allow=r'/forum/index.php/topic,[\d]+.0.html'), callback='parse_item', follow=False)

]
    
    def parse_item(self, response):
        forum_data = LycaeumItem()
        forum_data['Title'] = response.xpath('//h5//text()').extract()[1]
        forum_data['Text'] = response.xpath('//div[@class = "post_wrapper"]//div[@class = "inner"]/text()').extract()
        forum_data['Title'] =  str(forum_data['Title'])
        forum_data['Title'] =  str(forum_data['Title']).replace('\\' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace('?' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace('*' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace('>' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace('<' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace(':' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace('"' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace('/' , "")
        forum_data['Title'] =  str(forum_data['Title']).replace('|' , "")
        forum_data['Substance'] = ""
        yield forum_data