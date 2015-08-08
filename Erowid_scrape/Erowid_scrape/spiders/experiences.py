import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector

class ExperiencesSpider(CrawlSpider):
    name = "experiences"
    allowed_domains = ["www.erowid.org/experiences"]
    start_urls = ['http://www.erowid.org/experiences/exp_list.shtml','http://www.erowid.org/experiences/exp_list.shtml']
    rules = [
        Rule(LinkExtractor(allow=['/exp.php?ID=d*']), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=['/subs/exp_aPVP.shtml']))
    ]
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        #Experience = scrapy.Item()
        #Experience['Title'] = response.xpath('/div[@class="title"]/text()').extract
        #Experience['substance'] = response.xpath('/div[@class="substance"]/text()').extract()
        #Experience['author'] = response.xpath('/div[@class="author"]/text()').extract()
        #Experience['report-text-surround'] = response.xpath('/div[@class="report-text-surround"]/text()').extract()
        #yield Experience

        Title = hxs.select('/div[@class="title"]/text()')
        substance = hxs.select('/div[@class="substance"]/text()')
        author = hxs.select('/div[@class="author"]/text()')
        print Title,substance,author
