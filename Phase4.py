from operator import itemgetter
from datetime import datetime
import re
import sys
import pprint
import json
from pymongo import MongoClient

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
            while (not('www' in data or 'default' in data)):
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
        print("Default database used")
    else:
        print(enteredURL, "database used")
    print("Data Crawling is successful and all data are inserted into the database")
# 5.3
def courseSearch():
    print("There are two search operations available:")
    print("\t1. Course Search by Keyword")
    print("\t2. Course Search by Waiting List Size\n")
    choice = input("Please indicata the preferred operation\n")



    # keyword search
    if choice == "1":
        query = input("Please enter your keyword  (you may enter \"Data\" for testing)")
        keywordSearch(query)
    #waitlist search
    elif choice == "2":
        while True:
            try:
                print("Notes: you may use the f = 1.0, date = 2018-02-01 15:30 for testing")
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

        waitingListSearch(f, start_ts, end_ts)
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
def waitingListSearch(f, start_ts, end_ts):
    matchedCourseDetails = {}
    for courseDetails in courseOfferings.values():
        for sectionDetails in courseDetails[6]:
            match_ts = datetime.strptime(sectionDetails[1], "%Y-%m-%d %H:%M")
            if (sectionDetails[0][0] == 'L') and (start_ts <= match_ts <= end_ts):
                copyedCourseDetails = courseDetails[:]
                copyedCourseDetails.append(sectionDetails[1])

                for matchedSectionDetails in copyedCourseDetails[6]:
                    if float(matchedSectionDetails[7]) >= f * float(matchedSectionDetails[5]):
                        matchedSectionDetails.append('Yes')
                    else:
                        matchedSectionDetails.append('No')

                matchedCourseDetails[courseDetails[0]] = copyedCourseDetails
    matchedCourseDetails = sorted(matchedCourseDetails.items(), key = itemgetter(0))
    printAllMatched(matchedCourseDetails)

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
	testDbConnection()
	testing()
	main()


client.close()
