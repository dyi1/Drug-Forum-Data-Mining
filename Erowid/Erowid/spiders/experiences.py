import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

from Erowid.items import ErowidItem


class ExperiencesSpider(CrawlSpider):
    name = "experiences"
    allowed_domains = ["www.erowid.org"]
    start_urls = ['https://www.erowid.org/experiences/exp_list.shtml']
    rules = [ 
        Rule(LinkExtractor(allow =('subs/.*')), follow = True)    
    ]
    def parse_item(self, response):
        pass
       ##Will move the code over from test.py after