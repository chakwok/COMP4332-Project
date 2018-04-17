import scrapy
from datetime import datetime
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['coursesInsert']


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
		#print(Courses)
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
			#xpathToSections = "//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//table[@class = \"sections\"]//tr//td[1]/text()"
			
			
			#get attributes
			Attributes = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//tr[./th=\"ATTRIBUTES\"]//td/text()").extract()
			tempstring = ""
			for items in Attributes:
				tempstring = tempstring + str(items) + "\n"
			Attributes = tempstring
			Attributes = Attributes[0:-2]
			
			#Other optional attributes
			Exclusion = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//tr[./th=\"EXCLUSION\"]//td/text()").extract()
			tempstring = ""
			for items in Exclusion:
				tempstring = tempstring + str(items) + "\n"
			Exclusion = tempstring
			Exclusion = Exclusion[0:-1]
			
			Description = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//tr[./th=\"DESCRIPTION\"]//td/text()").extract()
			Vector = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//tr[./th=\"VECTOR\"]//td/text()").extract()
			
			Pre = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//tr[./th=\"PRE-REQUISITE\"]//td/text()").extract()
			tempstring = ""
			for items in Pre:
				tempstring = tempstring + str(items) + "\n"
			Pre = tempstring
			Pre = Pre[0:-1]
			
			Co = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//tr[./th=\"CO-REQUISITE\"]//td/text()").extract()
			tempstring = ""
			for items in Co:
				tempstring = tempstring + str(items) + "\n"
			Co = tempstring
			Co = Co[0:-1]
			
			Previous = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//tr[./th=\"PREVIOUS CODE\"]//td/text()").extract()
			
			#Sections = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//table[@class = \"sections\"]//tr//td/text()").extract()
			#print(Courses[i])
			#print(Exclusion)
		#get timeslot and semester from title
		head = response.xpath("//title/text()").extract_first()
		date = head[-16:]
		#get datetime format for timeslot of current snapshot
		recordTime = datetime.strptime(date, "%Y-%m-%d %H:%M")
		#get semester
		semester = head[0:14]
		
		# get setions
		Sections = response.xpath("//div[@class = \"course\" and ./div/a/@name =\""+Courses[i]+"\"]//table[@class = \"sections\"]//tr//td//text()").extract()
		print(Courses[i])
		print(Sections.index('\xa0'))
		#if (Sections.index('\xa0') != 8):

		print(Sections)
		
		#enable this part to insert the document after we fix Sections
		"""
		endOfSection = 0 
		try: 
			endOfSection = Sections.index('\xa0')
		except:
			endOfSection = Sections.index('Instructor Consent Required')

		oneSection = {
		'recordTime': recordTime,
		'sectionId': Sections[0],
		'offerings':[{
			'dateAndTime': Sections[endOfSection -7],
			'room': Sections[endOfSection -6],
			'Instructor': Sections[endOfSection-5],
		}],
		'quota': Sections[endOfSection-4],
		'enrol': Sections[endOfSection -3], 
		'wait': Sections[endOfSection -1] 
		}

		oneSection = oneSection.dumps(oneSection)

		
		# if the course(code) doesn't exist in the database, create a new document with the first section filled
		if (db.courses.find({"code": courses[i]}).count() != 1):
			db.courses.insert(
				{
					"code": Courses[i],
					"semester": semester,
					"title": titles[i],
					"credits": credits[i],
					"attributes": Attributes,
					"exclusion": Exclusion, 
					"description": Description,
					"sections": [{
						oneSection
					}]
				})
		else:
			db.courses.update({"code": Courses[i]},
				{"$push":{ "sections": oneSection} }
				)
		"""



		#to add multiple sections of a same course we need a while true loop to surround the above code
		"""
		while True:
			if (len(Sections) == endOfSection):
				break

			else:
				del Sections[:endOfSection]
		"""

		#print(Sections)
		#print(Courses[1])


		#print(Sections)
		
		'''
		with open(crawlFilename, "a") as f:
			for course in Courses:
				f.write(course)
				f.write("\n")
		'''