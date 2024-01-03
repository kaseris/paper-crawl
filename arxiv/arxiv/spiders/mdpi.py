import requests
import scrapy
from scrapy.http import HtmlResponse


"""
Mixed Palletising
Mixed Palletizing 
Mixed Palletisation
Mixed Palletization
Pallet loading problem 
3d bin packing problem - 3DBPP
"""

class MDPISpider(scrapy.Spider):
    name = 'MDPI'
    search_term = 'bin packaging problem'.lower().replace(' ', '+')
    start_urls = [f'https://www.mdpi.com/search?q={search_term}']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers={'Referer': 'https://www.mdpi.com/', **self.headers})
    
    def parse(self, response):
        print('\n', '='*100)
        print(response.json())
        print('\n', '='*100)
        
        clean_html = self.remove_more_elements(response.text)
        clean_response = HtmlResponse(url=response.url, body=clean_html, encoding='utf-8')
        papers = clean_response.css('div.generic-item.article-item')
        for paper in papers:
            title = paper.css('a.title::text').get()
            abstract = paper.css('div.abstract-full::text').get()
            yield {'title': title, 'abstract': abstract}
            
    def remove_more_elements(self, html: str):
        return html.replace('<span class="more" style="display: none;">', '').replace('</span>', '')
    
    #TODO: Simulate the request by:
    # 1. Issuing a HTML GET request to the start URL
    # 2. Count the number of results
    # 3. Issue ajax requests to the XHR url
    # 4. Repeat until we have n_results = n_shown_in_page