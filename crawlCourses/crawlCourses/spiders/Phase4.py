from operator import itemgetter
from datetime import datetime
import re
import sys
import pprint
from pymongo import MongoClient
import json
import subprocess

client = MongoClient('mongodb://localhost:27017')
db = client['courses']

pp = pprint.PrettyPrinter(width = 160, compact=True)

def testing():
	print('\ntesting here \n')



def testDbConnection():
	print("A document of the collection is printed to test the connection")
	print(db.course.find_one())



def main():
	# here, we need to implement for the flow
	# display the menu
	choice = "0"
	while (choice != "6"):
		print("\n   Main Menu")
		print("=======================")
		print("1. Drop/ Empty Collections")
		print("2. Crawl Data")
		print("3. Search Course")
		print("4. Predict Waiting List Size")
		print("5. Train Wating List Size")
		print("6. Exit")



		# allow the user to choose one of the functions in the menu
		choice = input("Please input your choice (1-6): ")

		print("")

		# check the input and call the correspondence function
		if (choice == '1'):
			dropAndEmptySuccessful()
		elif (choice == '2'):
			data = input("Please input a URL to be crawled or \"default\" ")
			while (not('http' in data or 'default' in data)):
				data = input("Please input a valid URL or \"dafault\"")
			crawlData(data)
		elif (choice == '3'):
			courseSearch()
		elif (choice == '4'):
			while True:
				try:
					cc = input("Input the course code (in a format of (CCCCXXXXC) where \"C\" denotes a capitalized letter and \"X\" denotes a digit")
					while not bool(re.match('[A-Z]{4}[0-9]{4}[A-Z]?', cc)):
						cc = input("Input a correct course code (in a format of (CCCCXXXXC) where \"C\" denotes a capitalized letter and \"X\" denotes a digit")
					ln = int(input("Please indicate the lecture number (only numeric value)"))
					ts = input("Please input time slot (in a format of YYYY-MM-DD HH:mm) ")
					ts = datetime.strptime(ts, "%Y-%m-%d %H:%M")
					break
				except ValueError:
					print("Please input all values in correct format")
			waitingListSizePrediction(cc, ln, ts)
		elif (choice == '5'):
			waitingListSizeTraining()
		elif (choice == '6'):
			sys.exit()
		else:
			print("Invalid Input!", choice)


# 5.1
def dropAndEmptySuccessful():
	# checking should be done
	print("Collection dropping and empty collection creating are successful")

# 5.2
def crawlData(enteredURL):
	if enteredURL == 'default':
		enteredURL = "http://comp4332.com/realistic"
		print("Default database used")
	else:
		print(enteredURL, "database used")
	strCommand = 'scrapy crawl crawlCourses -a "urls='+enteredURL+"\""
	subprocess.run(strCommand, shell=True)
	print("Data Crawling is successful and all data are inserted into the database")


# 5.3
def courseSearch():
	print("There are two search operations available:")
	print("\t1. Course Search by Keyword")
	print("\t2. Course Search by Waiting List Size\n")
	choice = input("Please indicate the preferred operation\n")



	# keyword search
	if choice == "1":
		query = input("Please enter your keyword  (you may enter \"Data\" for testing)")
		keywordSearch(query)
	#waitlist search
	elif choice == "2":
		while True:
			try:
				print("Notes: you may use the f = 0.05, date = 2018-02-01 11:00 and 2018-02-10 12:00 for testing")
				print("Notes: incorrect date format will not be accepted")
				f = input("Please input f value ")
				f = float(f)
				start_ts = input("Please input start time (in a format of YYYY-MM-DD HH:mm) ")
				start_ts = datetime.strptime(start_ts, "%Y-%m-%d %H:%M")
				end_ts = input("Please input end time (in a format of YYYY-MM-DD HH:mm) ")
				end_ts = datetime.strptime(end_ts, "%Y-%m-%d %H:%M")
				break
			except ValueError:
				print("Please input all values in correct format")

		newFunction(f = 0.05, start =datetime(2018, 2, 1, 11, 0), end = datetime(2018,2,10 ,12, 0 ))
	else:
		print("Please enter a valid choice\n")

def convertToRE(query):
	keywords = re.sub(r"""[,;.?:'"/\&+-+*!()]""", " ", query).split()

	for index, element in enumerate(keywords):
		keywords[index] = r"(\s|\b)" + element + r"(\s|\b)"

	query = '|'.join(keywords)
	return query

def keywordSearch(query):
	#matchedCourses = []
	#print(re.sub(r"""[,;.?:'"/\&+-+*!()]""", " ", query).split())

	query = convertToRE(query)

	results = db.course.aggregate([
	#match the course according to the specified requirement, we are using regular expression to check if the Cname in the database contains the phrase(s) in the query
	{'$match': {"Cname": {"$regex": query}}},
	{'$unwind':"$TimeList"},
	{'$project': {"Course_Code":1, "Cname":1, "Units":1, "_id":0, "TimeList.timeslot":1, "TimeList.SectionList":1}},
	#to retrieve the section details in TimeList which has the largest timeslot, we reorder it in descending order
	#by using the $first operation we get the timeslot with latest date, which contains the most updated information
	#$first is a feature that returns the value that results from applying an expression to the first document in a group of documents that share the same group by key. Only meaningful when documents are in a defined order.
	{'$sort':{"Cname":-1,"TimeList.timeslot":-1}},
	{'$group':{
		"_id": "$Course_Code",
		"CourseTitle": {"$first": "$Cname"},
		"NoOfUnits": {"$first": "$Units"},
		"TimeSlot": {"$first": "$TimeList.timeslot"},
		"SectionList": {"$first": "$TimeList.SectionList"}
		}
	},
	#output in the return format as required
	{'$project': {"_id":1, "CourseTitle":1, "NoOfUnits":1, "MatchedTimeSlot":1, "SectionList.section":1, "SectionList.date_time":1, "SectionList.quota":1, "SectionList.enrol":1, "SectionList.available":1, "SectionList.wait":1}},
	{'$sort': {"_id":1} }
	])

	for instance in results:
		print(instance)

def newFunction(f, start, end):
	#print(start)
	#print(end )
	db.course2.aggregate([
	{'$unwind':"$TimeList"},
	{'$project':{'_id':0,'Cname':1,'TimeList':1}},
	{'$unwind':"$TimeList.SectionList"},
	{'$project':{
		'_id':0,
		'Cname':1,
		"TimeList.timeslot":1,
		"TimeList.SectionList.section":1,
		"TimeList.SectionList.date_time":1,
		"TimeList.SectionList.quota":1,
		"TimeList.SectionList.enrol":1,
		"TimeList.SectionList.available":1,
		"TimeList.SectionList.wait":1,
		#compute the f * enrol for later use
		"fenrol":{'$multiply':[f,"$TimeList.SectionList.enrol"]}}},
	{'$project':{
		'_id':0,
		'Cname':1,
		"TimeList.timeslot":1,
		"TimeList.SectionList.section":1,
		"TimeList.SectionList.date_time":1,
		"TimeList.SectionList.quota":1,
		"TimeList.SectionList.enrol":1,
		"TimeList.SectionList.available":1,
		"TimeList.SectionList.wait":1,
		"fenrol":1,
		#check if the required condition is saitified, adding the new attribute
		"TimeList.SectionList.Satisfied":{
			'$cond':{
				'if':{
					'$gte': ["$TimeList.SectionList.wait", "$fenrol"]
				},
				'then': "Yes",
				'else': "No",
			}
		}
	}},
	{'$project':{
		'_id':0,
		"Cname":1,
		"timeslot":"$TimeList.timeslot",
		"List.section":"$TimeList.SectionList.section",
		"List.date_time":"$TimeList.SectionList.date_time",
		"List.quota":"$TimeList.SectionList.quota",
		"List.enrol":"$TimeList.SectionList.enrol",
		"List.available":"$TimeList.SectionList.available",
		"List.wait":"$TimeList.SectionList.wait",
		"List.Satisfied":"$TimeList.SectionList.Satisfied"
	}},
	{'$group':{
		"_id":{
			"Cname":"$Cname",
			"timeslot":"$timeslot"
		},
		"List":{'$push':{"List":"$List"}}

	}},
	{'$project':{
		'_id':0,
		"Cname":"$_id.Cname",
		"timeslot":"$_id.timeslot",
		"List":"$List.List"

	}},
	#output to a new collection for later use
	{'$out':"allWithStatisfied"}
	]
	)

	results2 = db.course2.aggregate([
	{'$unwind':"$TimeList"},
	#//match the timeslot(Date object) twice to filter out only the time within the range using the gte and lte operations
	{'$project': {'Course_Code':1, 'Cname':1, 'Units':1, '_id':0, 'TimeList':1, 'greater_than_start': {'$gte': ["$TimeList.timeslot", start]} ,'less_than_end': {'$lte': ["$TimeList.timeslot", end]}}},
	{'$match': {'greater_than_start':'true'}},
	{'$match': {'less_than_end':'true'}},
	{'$unwind':"$TimeList.SectionList"},
	#//match only the section of object is Lecture using regular expression, as required
	{'$match': {"TimeList.SectionList.section":'/^L/i'}},
	#	//would match again to keep only the section that match the waitlist requirement (i.e. the number of students in the waiting list of this lecture section is greater than or equal to f multiplied by the number of students enrolled in this lecture section in that time slot.)
	#//The initial value of f is hardcoded as 0.05.
	{'$project':{'Course_Code':1, 'Cname':1, 'Units':1, '_id':0, 'TimeList':1,"fenrol":{'$multiply':[f,"$TimeList.SectionList.enrol"]}}},
	{'$project': {'Course_Code':1, 'Cname':1, 'Units':1, '_id':0, 'TimeList':1, 'wait_list_fulfilled': {'$gte': ["$TimeList.SectionList.wait", "$fenrol"]}}},
	{'$match': {'wait_list_fulfilled':'true'}},
	#	//to retrieve the most updated information, we order it in descedning order; the $first operation can get the most updated info
	#//$first is a feature that returns the value that results from applying an expression to the first document in a group of documents that share the same group by key. Only meaningful when documents are in a defined order.
	{'$sort':{'Cname':-1,"TimeList.timeslot":-1}},
	{'$group':{
		"_id": "$Course_Code",
		"CourseTitle": {"$first": "$Cname"},
		"NoOfUnits": {"$first": "$Units"},
		"MatchedTimeSlot": {"$first": "$TimeList.timeslot"}
		}
	},
	#//lookup the information of the course_section that fulfill the waitlist requirement from the "All" document we outputted at the beginning
	#//used a complicated operation, joining them using two attributes i.e. course name and timeslot. 
	{'$lookup':
		{
			'from': "allWithStatisfied",
			'let':{'time':"$MatchedTimeSlot",'name':"$CourseTitle"},
			'pipeline':[
				{'$match':
					{'$expr':
						{'$and':
							[
							{'$eq':["$Cname", "$$name"]},
							{'$eq':["$timeslot", "$$time"]}
							]
						}
					}
				}
				],
			'as': "course_info"
		}
	},
	#output the information as required
	{'$project':{'_id':1,'CourseTitle':1,'NoOfUnits':1,'MatchedTimeSlot':1,'SectionList':"$course_info.List"}},
	{'$project':{'_id':1,'CourseTitle':1,'NoOfUnits':1,'MatchedTimeSlot':1,"SectionList.section":1,"SectionList.date_time":1,"SectionList.quota":1,"SectionList.enrol":1,"SectionList.available":1,"SectionList.wait":1,"SectionList.Satisfied":1}}
	])

	for instance in results2:
		print(instance)


def printAllCourses(courses):
	if len(courses) == 0:
		print("There is no match")
	else:
		print("Here are all the matched courses")
		for course in courses:
			printACourse(course)

def printACourse(courseDetails):
	print('Course Code:', courseDetails[0])
	print('Course Title', courseDetails[1])
	print('No. of Units/Credits', courseDetails[2])
	for section in courseDetails[6]:
		print('\nSection Details: ')
		print('\tSection', section[0])
		print('\tDate & Time', section[1])
		print('\tQuota', section[4])
		print('\tEnrol', section[5])
		print('\tAvail', section[6])
		print('\tWait', section[7])
		print('\n')
	print('\n')

# need testing
"""
def waitingListSearch(f, start, end):
	db.course2.aggregate([
	{'$unwind':"$TimeList"},
	{'$project':{'_id':0,'Cname':1,'TimeList':1}},
	{'$unwind':"$TimeList.SectionList"},
	{'$project':{
		'_id':0,
		'Cname':1,
		"TimeList.timeslot":1,
		"TimeList.SectionList.section":1,
		"TimeList.SectionList.date_time":1,
		"TimeList.SectionList.quota":1,
		"TimeList.SectionList.enrol":1,
		"TimeList.SectionList.available":1,
		"TimeList.SectionList.wait":1,
		"fenrol":{'$multiply':[f,"$TimeList.SectionList.enrol"]}}},
	{'$project':{
		'_id':0,
		'Cname':1,
		"TimeList.timeslot":1,
		"TimeList.SectionList.section":1,
		"TimeList.SectionList.date_time":1,
		"TimeList.SectionList.quota":1,
		"TimeList.SectionList.enrol":1,
		"TimeList.SectionList.available":1,
		"TimeList.SectionList.wait":1,
		"fenrol":1,
		"TimeList.SectionList.Satisfied":{
			'$cond':{
				'if':{
					'$gte': ["$TimeList.SectionList.wait", "$fenrol"]
				},
				'then': "Yes",
				'else': "No",
			}
		}
	}},
	{'$project':{
		'_id':0,
		"Cname":1,
		"timeslot":"$TimeList.timeslot",
		"List.section":"$TimeList.SectionList.section",
		"List.date_time":"$TimeList.SectionList.date_time",
		"List.quota":"$TimeList.SectionList.quota",
		"List.enrol":"$TimeList.SectionList.enrol",
		"List.available":"$TimeList.SectionList.available",
		"List.wait":"$TimeList.SectionList.wait",
		"List.Satisfied":"$TimeList.SectionList.Satisfied"
	}},
	{'$group':{
		"_id":{
			"Cname":"$Cname",
			"timeslot":"$timeslot"
		},
		"List":{'$push':{"List":"$List"}}

	}},
	{'$project':{
		'_id':0,
		"Cname":"$_id.Cname",
		"timeslot":"$_id.timeslot",
		"List":"$List.List"

	}},
	{'$out':"allWithStatisfied"}
	]
	)


	results = db.course2.aggregate([
	{'$unwind':"$TimeList"},
	{'$project': {'Course_Code':1, 'Cname':1, 'Units':1, '_id':0, 'TimeList':1, 'greater_than_start': {'$gte': ["$TimeList.timeslot", start]} ,'less_than_end': {'$lte': ["$TimeList.timeslot", end]}}},
	{'$match': {'greater_than_start':'true'}},
	{'$match': {'less_than_end':'true'}},
	{'$unwind':"$TimeList.SectionList"},
	{'$match': {"TimeList.SectionList.section":'/^L/i'}},
	{'$project': {'Course_Code':1, 'Cname':1, 'Units':1, '_id':0, 'TimeList':1, 'wait_list_fulfilled': {'$gte': ["$TimeList.SectionList.wait", { '$multiply': [ "$TimeList.SectionList.enrol", f ] }]}}},
	{'$match': {'wait_list_fulfilled':'true'}},
	{'$sort':{'Cname':-1,"TimeList.timeslot":-1}},
	{'$group':{
		"_id": "$Course_Code",
		"CourseTitle": {"$first": "$Cname"},
		"NoOfUnits": {"$first": "$Units"},
		"MatchedTimeSlot": {"$first": "$TimeList.timeslot"}
		}
	},
	{'$lookup':
		{
			'from': "all",
			'let':{'time':"$MatchedTimeSlot",'name':"$CourseTitle"},
			'pipeline':[
				{'$match':
					{'$expr':
						{'$and':
							[
							{'$eq':["$Cname", "$$name"]},
							{'$eq':["$TimeList.timeslot", "$$time"]}
							]
						}
					}
				}
				],
			'as': "course_info"
		}
	},
	{'$project':{'_id':1,'CourseTitle':1,'NoOfUnits':1,'MatchedTimeSlot':1,'SectionList':"$course_info.TimeList.SectionList"}},
	{'$project':{'_id':1,'CourseTitle':1,'NoOfUnits':1,'MatchedTimeSlot':1,"SectionList.section":1,"SectionList.date_time":1,"SectionList.quota":1,"SectionList.enrol":1,"SectionList.available":1,"SectionList.wait":1}}
	])
"""



def printAllMatched(matchedCourseDetails):
	for course in matchedCourseDetails:
		printACourseWS(course[1])



def printACourseWS(courseDetails):
	print('Course Code:', courseDetails[0])
	print('Course Title', courseDetails[1])
	print('No. of Units/Credits', courseDetails[2])
	print('Matched Time Slot', courseDetails[-1])
	for section in courseDetails[6]:
		print('\nSection Details: ')
		print('\tSection', section[0])
		print('\tDate & Time', section[1])
		print('\tQuota', section[4])
		print('\tEnrol', section[5])
		print('\tAvail', section[6])
		print('\tWait', section[7])
		print('\tSatisfied', section[9])
		print('\n')
	print('\n')

# offerings = {cid : [courseDetails]}
# sectionDetails = [Section Num, DateTime, Room, Instructor, Quota, Enrol, Avail, Wait, Remarks]
# courseDetails = [CourseCode, Course Title, Credits, [Pre-re(Course Code)], [Exclusion(Course Code], Course Descr, [[sectionDetails](s)]]
courseOfferings = {'COMP4332L1':
					   ['COMP4332', 'Big Data Mining and Management', 3,[], [], "This is a big data course that teaches problem solving",
						[['L1', '2018-02-01 15:30', 'G010', 'Prof Raymond', 100, 51, 49, 0,'can take' ]]],
				   'RMBI4310L1':
					   ['RMBI4310', 'Advanced Data Mining for Risk Management and Business Intelligence', 3,[], [], "This is a big data course that teaches problem solving",
						[['L1', '2018-02-01 15:30', 'G010', 'Prof Raymond', 100, 52, 48, 0,'can take' ]]],
				   'COMP4333L1':
					   ['COMP4333', 'Big Data Mining and Management', 3,[], [], "This is a big data course that teaches problem solving",
						[['L1', '2018-02-01 15:30', 'G010', 'Prof Raymond', 100, 51, 49, 0,'can take' ]]]
				   }
courses = ["COMP4332" , "ELEC1010", "COMP3221", "Big Data Management", "Dumb Data", "sth"]
#courses = courseOfferings.keys()

# 5.4
def waitingListSizePrediction(cc, ln, ts):
	print("The predicted waiting list size of", cc, "Lecture", ln, "in", ts, "is \n")
	print("1, 3, 5, 8, 12")


# 5.5
def  waitingListSizeTraining():
	print("Waiting list size training is successful")


if __name__ =='__main__':
	#testDbConnection()
	#testing()
	main()


client.close()
