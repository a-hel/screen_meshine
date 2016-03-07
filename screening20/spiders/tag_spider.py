import scrapy

from screening20.items import TermItem

from bs4 import BeautifulSoup
import requests
import re


        
class TagSpider(scrapy.Spider):
    name = 'tagspider'
    tags = ['health', 'flu']
    lang = 'en'
    #start_urls = ['https://%s.wordpress.com/tag/%s' % (lang, tag) for tag in tags]
    start_urls = ['https://public-api.wordpress.com/rest/v1.1/read/tags/%s/posts' % 'flu',]

    def parse(self, response):
        # Get blogs entries with tags
        print response
        #for href in response.css("a[class='post-title']::attr('href')"):# > a::attr('href')"):
        #    url = href.extract()
        #    yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
    	"""Get blog entries from url"""

        scraped_terms = [_extract_terms(url) for url in response.css("div[class='entry-content']")]
        with open('resfile.txt', 'a') as f:
            for scraped_term in scraped_terms:
    			f.write(','.join(scraped_term))
    			f.write('\n')
    	
            #term_item = TermItem()
            #term_item.url = href.referrer
            #term_item['name'] = 'name'
            #term_item['mesh_terms'] = extracted
            #term_item['mesh_terms_l'] = extracted		
    		#yield term_item
    		#print extracted


def _decompile_terms(response):
    """Find mesh terms from raw html using regexp"""
    
    exp = '(?<=term=)[\w ]*(?=" target)'
    res = re.findall(exp, response)
    term_list = list(set(res))
    return term_list

def _get_mesh_terms(raw_text):
    """extract mesh terms from raw_text"""
    
    mesh_url = r"http://ii.nlm.nih.gov/cgi-bin/II/Interactive/MeSHonDemand.pl"
    response = requests.post(mesh_url, data=raw_text)
    response_encoded = response.text.encode('utf-8')
    terms = _decompile_terms(response_encoded)
    return terms


def _extract_terms(url):
    """Return MeSH terms from url"""

    tagged_body = url.extract()
    naked_body = BeautifulSoup(tagged_body, 'html.parser').get_text()
    raw_data = {"InputText": naked_body.encode('utf-8')}
    mesh_terms = _get_mesh_terms(raw_data)
    return mesh_terms