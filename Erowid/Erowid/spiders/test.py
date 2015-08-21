import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from Erowid.items import ErowidItem


#filename = img_alt + '.jpg'
#with open(os.path.join(path, filename), 'wb') as temp_file:
    #temp_file.write(buff)


class ExperiencesSpider(CrawlSpider):
    name = "test"
    allowed_domains = ["www.erowid.org"]
    start_urls = ['https://www.erowid.org/experiences/subs/exp_aPVP.shtml']
    rules = [
    Rule(LinkExtractor(allow=r'/experiences/exp\.php\?ID=\d+$'),
         callback='parse_item', follow=True)
]
    def parse_item(self, response):
        selectors = response.css('div')
        for selector in selectors:
            experience = ErowidItem()
            experience['Author'] = selector.xpath('//div[@class="author"]/a/text()').extract()
            experience['Title'] = selector.xpath('//div[@class="title"]/text()').extract()
            experience['Substance'] = selector.xpath('//div[@class="substance"]/text()').extract()
            experience['Text'] = selector.xpath("//div[@class = 'report-text-surround']/text()").extract()
            ##use strip to remove extra spaces
            ##[3:-2] Removes the extra parts in the beginning
            experience['Author'] = str(experience['Author'])[3:-2].strip()
            experience['Substance'] = str(experience['Substance'])[3:-2].strip()
            experience['Title'] = str(experience['Title'])[3:-2].strip()
            
            ##Removed non-text and formatting 
            experience['Text'] = str(experience['Text'])[3:-2].replace("\\n\'", "")
            experience['Text'] = str(experience['Text']).replace('"', "")
            experience['Text'] = str(experience['Text']).replace(", u'", "")
            experience['Text'] = str(experience['Text']).replace(", u\\n'", "")
            experience['Text'] = str(experience['Text']).replace(", u\\n", "")
            experience['Text'] = str(experience['Text']).replace("'\\n", "")
            experience['Text'] = str(experience['Text']).replace("\\n", "")
            experience['Text'] = str(experience['Text']).replace("\\r'", "")
            experience['Text'] = str(experience['Text']).replace("\\r", "")
            experience['Text'] = str(experience['Text']).replace("\\t'", "")
            experience['Text'] = str(experience['Text']).replace("\\t", "")
            experience['Text'] = str(experience['Text']).replace(", u", "")
            
            
            filename = str(experience['Substance']) + " "+ str(experience['Title'])
            with open(filename,"w") as fid:
                fid.write(str(experience) + "\n")
##Need to fix the above formatting