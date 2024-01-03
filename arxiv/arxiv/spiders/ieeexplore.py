import datetime
import json
import requests
from typing import Any
import scrapy

from bs4 import BeautifulSoup

from ..settings import USER_AGENT


"""
Mixed Palletising
Mixed Palletizing 
Mixed Palletisation
Mixed Palletization
Pallet loading problem 
3d bin packing problem - 3DBPP
"""

class IEEEXploreSpider(scrapy.Spider):
    name = 'IEEEXplore'
    start_urls = ['https://ieeexplore.ieee.org/rest/search']
    
    headers = {
        'Referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22All%20Metadata%22:mixed%20palettizing)',
        "Content-Type": "application/json; charset=utf8",
    }
    
    payload = {
        'action': 'search',
        'newsearch': True,
        'matchBoolean': True,
        'queryText': '(\"All Metadata\": mixed palletizing)',
        'highlight': False,
        'returnFacets': ['ALL'],
        'returnType': 'SEARCH',
        'matchPubs': True,
        'pageNumber': 1
    }
    
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            headers=self.headers,
            body=json.dumps(self.payload),
            callback=self.parse
        )
    
    def parse(self, response):
        try:
            json_data = json.loads(response.body)
            papers_info = json_data['records']
            for paper in papers_info:
                document_link = paper['documentLink']
                url = f'https://ieeexplore.ieee.org{document_link}'
                req = requests.get(url, headers={'User-Agent': USER_AGENT})
                if req.status_code == 200:
                    soup = BeautifulSoup(req.text, 'html.parser')
                    abstract = soup.find('meta', property='og:description')['content']
                title = paper['articleTitle']
                publication_year = int(paper['publicationYear'])
                citations = int(paper['citationCount'])
                yield {'document_link': document_link, 'title': title, 'publication_year': publication_year, 'abstract': abstract, 'citations': citations}
            
            total_pages = json_data['totalPages']
            for page_number in range(2, total_pages + 1):
                next_page = page_number
                yield scrapy.Request(
                    url=self.start_urls[0],  
                    method='POST',
                    headers=self.headers,
                    body=json.dumps({**self.payload, 'pageNumber': next_page}),
                    callback=self.parse,
                    meta={'current_page': page_number}
                    )
                   
        except json.decoder.JSONDecodeError as e:
            print(f'JSONDecodeError:  {e}')
            