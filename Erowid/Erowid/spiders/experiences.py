import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from Erowid.items import ErowidItem
import os

class ExperiencesSpider(CrawlSpider):
    name = "experiences"
    allowed_domains = ["www.erowid.org"]
    start_urls = ['https://www.erowid.org/experiences/exp_list.shtml']
    
    rules = [Rule(LinkExtractor(allow =('subs/exp_[a-zA-Z]+.shtml')),callback='parse_item', follow = True)

#        Rule(LinkExtractor(allow =('subs/exp_[a-zA-Z]+.shtml')), follow = True)    

   ]
    def parse_item(self, response):
        filename = str(response.url)[44:-6]
        selectors = response.css('table')
        if not os.path.exists('drugs-%s' % (filename)): ##Make the file
            os.makedirs('drugs-%s' % (filename))
        list_of_experience = selectors.xpath('//table[@class="exp-cat-table"]/tr/td/a/@href').extract()
        
        for item in list_of_experience:
            request_url = str(item)
            
            Request(url="http://www.erowid.org" + request_url, callback = 'request_experience')
            
            def request_experience(self, response):
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
            
            
                    title = str(experience['Substance']) + " "+ str(experience['Title'])
                    print experience
                    with open(os.path.join('drugs-%s' % (filename), title),"w") as fid:
                        fid.write(str(experience) + "\n")            
                
                
        
        #sos.chdir(os.pardir)##Back to previous file
        '''
        
        for item in list_of_experience:
            with open(os.path.join('drugs-%s' % (filename), filename),"a") as fid:
                fid.write(item + "\n")
            

       ##Will move the code over from test.py after
        '''