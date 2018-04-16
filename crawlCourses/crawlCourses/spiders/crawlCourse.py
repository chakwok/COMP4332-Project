import scrapy
from datetime import datetime

class LinkWebpageSpider(scrapy.Spider):
	name = "crawlCourses"
	
	def __init__(self, *args, **kwargs):
		urls = kwargs.pop('urls', []) 
		if urls:
			self.start_urls = urls.split(',')
		self.logger.info(self.start_urls)
		super(LinkWebpageSpider, self).__init__(*args, **kwargs)
	
	def parse(self,response):
		listToTimeslot = response.xpath("//a[@href]/@href").extract()
		for link in listToTimeslot:
			yield response.follow(link, callback=self.toMajor)
				
	def toMajor(self,response):
		listToMajor = response.xpath("//a[@href]/@href").extract()
		for link in listToMajor:
			yield response.follow(link, callback=self.toCourse)
	
	def toCourse(self,response):
		crawlFilename = 'course.txt'
		
		#get course list
		Courses = response.xpath("//div[@class=\"courseanchor\"]/a/@name").extract()
		
		Description = response.xpath("//tr[th= \"DESCRIPTION\"]//td/text()").extract()
		
		#get course title
		temptitles = response.xpath("//h2/text()").extract()
		titles = [None]*len(temptitles)
		credits = [0]*len(temptitles)
		for i in range(len(temptitles)):
			titles[i] = temptitles[i][12:-9]
			#get course credits
			if(temptitles[i][-2]=='s'):
				credits[i]=int(temptitles[i][-8])
			else:
				credits[i]=int(temptitles[i][-7])
			#xpathToSections = "//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//table[@class = \"section\"]//tr//td[1]"
			#Sections = response.xpath("//div[@class = \"course\"]//table[@class = \"sections\"]//tr/td[1]/text()").extract()
			#print(Sections)
		#get timeslot and semester from title
		head = response.xpath("//title/text()").extract_first()
		date = head[-16:]
		#get datetime format for timeslot of current snapshot
		recordTime = datetime.strptime(date, "%Y-%m-%d %H:%M")
		#get semester
		semester = head[0:14]
		
		
		
		'''
		with open(crawlFilename, "a") as f:
			for course in Courses:
				f.write(course)
				f.write("\n")
		'''