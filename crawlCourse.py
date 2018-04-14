import scrapy

class LinkWebpageSpider(scrapy.Spider):
	name = "LinkWebpage"
	
	def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', []) 
        if urls:
            self.start_urls = urls.split(',')
        self.logger.info(self.start_urls)
        super(MySpider, self).__init__(*args, **kwargs)
	
	def parse(self,response):
		crawlFilename = 'timeslots.txt'
		listOfLink = response.xpath("//a[@href]/@href").extract()
		with open(crawlFilename = 'w') as f:
			f.write(listOfLink)