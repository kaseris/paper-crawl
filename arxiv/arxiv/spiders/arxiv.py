import datetime
import re
from typing import Any
import scrapy


class ArxivSpider(scrapy.Spider):
    name = "Arxiv"
    search_term = "3d bin packing problem"
    search_term = search_term.replace(" ", "+").lower()
    size = 200
    start_urls = [f"https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={search_term}&terms-0-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size={size}&order=-announced_date_first",]
    xpath = '//*[@id="main-container"]/div[2]/nav[1]/a[2]/@href'
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parset_out_html(self, string):
        string = string.strip().replace("\n", "").strip(' ')
        string = re.sub(r'<[^>]*>', '', string)
        string = string.strip()
        return string
    
    def parse(self, response):
        for paper in response.css('li.arxiv-result'):
            title = paper.css('p.title').get()
            abstract = paper.css('p.abstract').css('span.abstract-full::text').get()
            submitted_date = paper.css('p.is-size-7::text').get().replace(';', '')
            
            
            yield {'title': self.parset_out_html(title),'abstract': self.parset_out_html(abstract),
                    'submitted_date': self.parset_out_html(submitted_date),
                    'scraped_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),}
        
        next_page = response.xpath(self.xpath).get()
        if next_page:
            print(f'\nNext page: {"https://arxiv.org" + next_page};\n')
            yield scrapy.Request(url=f"https://arxiv.org{next_page}", callback=self.parse)
        else:
            print('No more pages.\n')