from operator import itemgetter
from datetime import datetime
import re
import sys



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
        query = input("Please enter your keyword\n (you may enter \"Data\" for testing)")
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

def keywordSearch(query):
    matchedCourses = []
    keywords = query.split()
    for keyword in keywords:
        for course in courseOfferings.values():
            courseKeywords = course[1].split()
            for courseKeyword in courseKeywords:
                if courseKeyword == keyword:
                    matchedCourses.append(course)
    matchedCourses = sortCoursesUsingCourseCode(matchedCourses)
    printAllCourses(matchedCourses)


def sortCoursesUsingCourseCode(courses):
    return sorted(courses, key = itemgetter(0))


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
        match_ts = datetime.strptime(sectionDetails[1], "%Y-%m-%d %H:%M")
        for sectionDetails in courseDetails[6]:
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

main()
