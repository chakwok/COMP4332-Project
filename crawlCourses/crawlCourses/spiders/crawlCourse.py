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
		listOfLink = response.xpath("//a[@href]/@href").extract()
		for link in listOfLink:
			yield response.follow(link, callback=self.toMajor)
				
	def toMajor(self,response):
		listOfLink = response.xpath("//a[@href]/@href").extract()
		for link in listOfLink:
			yield response.follow(link, callback=self.toCourse)
	
	def toCourse(self,response):
		crawlFilename = 'course.txt'
		listOfLink = response.xpath("//h2/text()").extract()
		#print(listOfLink)
		with open(crawlFilename, "a") as f:
			for link in listOfLink:
				f.write(link)
				f.write("\n")