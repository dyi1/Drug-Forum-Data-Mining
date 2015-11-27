# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import codecs
class LycaeumPipeline(object):
    def process_item(self, item, spider):
        cargo =  {
              'text': item['Text'],
    			 'substance': item['Substance'],
              'title' : item ['Title'] }
        
        

        directory = os.path.join('Lycaeum/forums/',cargo['title'].strip().lower())
        filename = os.path.join(directory,cargo['title']+'.txt') #

        if not os.path.exists(directory):
            os.makedirs(directory)

        with codecs.open(filename, encoding = 'utf-8', mode= 'wb') as fid:
            for symbols in cargo['text']:
                print>>fid,symbols 