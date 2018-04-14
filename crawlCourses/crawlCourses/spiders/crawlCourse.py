import scrapy

class LinkWebpageSpider(scrapy.Spider):
	name = "crawlCourses"
	
	def __init__(self, *args, **kwargs):
		urls = kwargs.pop('urls', []) 
		if urls:
			self.start_urls = urls.split(',')
		self.logger.info(self.start_urls)
		super(LinkWebpageSpider, self).__init__(*args, **kwargs)
	
	def parse(self,response):
		crawlFilename = 'timeslots.txt'
		listOfLink = response.xpath("//a[@href]/@href").extract()
		#print(listOfLink)
		with open(crawlFilename, "w") as f:
			for link in listOfLink:
				f.write(link)
				f.write("\n")