import scrapy

from screening20.items import TermItem

from bs4 import BeautifulSoup
import requests
import re


        
class TagSpider(scrapy.Spider):
    name = 'tagspider'
    lang = 'en'
    tags = ['health', 'flu']
    start_urls = ['https://%s.wordpress.com/tag/%s' % (lang, tag) for tag in tags]
    

    def parse(self, response):
		# Get blogs entries with tags
    	for href in response.css("a[class='post-title']::attr('href')"):# > a::attr('href')"):
    		url = href.extract()
    		yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
    	"""Get blog entries from url"""
    	with open('resfile.txt', 'a') as f:
	    	for href in response.css("div[class='entry-content']"):
    			tagged_body = href.extract()
    			naked_body = BeautifulSoup(tagged_body, 'html.parser').get_text()
    		
    		
    			data = {"InputText": naked_body.encode('utf-8')}
	    		mesh_url = r"http://ii.nlm.nih.gov/cgi-bin/II/Interactive/MeSHonDemand.pl"
    			resp = requests.post(mesh_url, data=data)
    			terms = resp.text
    			terms = terms.encode('utf-8')
    			terms_by_line = terms.split('\n')
    			if terms:
    				extracted = []
    				regex = re.compile('^<a href="https://www.nlm.nih.gov/cgi/mesh/2016/MB_cgi\?term=[\w ]+" target')
	    			for termline in terms_by_line:
    					pos = regex.match(termline)#.group()[59:-8]
    					if pos: extracted.append(pos.group()[59:-8])
    				term_item = TermItem()
    				#term_item.url = href.referrer
	    			term_item['name'] = 'name'
    				term_item['mesh_terms'] = extracted
    				term_item['mesh_terms_l'] = extracted
    				f.write(','.join(extracted))
    				f.write('\n')
    			
    				yield term_item
    			#print extracted

