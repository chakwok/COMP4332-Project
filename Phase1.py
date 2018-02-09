from operator import itemgetter
from datetime import datetime

# Q: Should it be implemented in OOP
# Todo: using Add exception block for strptime
# Todo:

URL = None
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


# 5.1
def dropAndEmptySuccessful():
    print("Collection dropping and empty collection creating are successful")

# 5.2
def crawlData(enteredURL):
    if enteredURL == "default":
        print("Data Crawling is successful and all data are inserted into the database")
    else:
        URL = enteredURL
        print("Data Crawling is successful and all data are inserted into the database")

# 5.3
def courseSearch():
    print("There are two search operations available:")
    print("\t1. Course Search by Keyword")
    print("\t2. Course Search by Waiting List Size\n")
    choice = input("Please indicata the preferred operation\n")



    # keyword search
    if choice == "1":
        query = input("Please enter your keyword\n")
        keywordSearch(query)
    #waitlist search
    elif choice == "2":
        f = input("Please input f value")
        start_ts = input("Please input start time (in a format of YYYY-MM-DD HH:mm)")
        end_ts = input("Please input end time (in a format of YYYY-MM-DD HH:mm)")
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
    f = float(f)
    start_ts = datetime.strptime(start_ts, "%Y-%m-%d %H:%M")
    end_ts = datetime.strptime(end_ts, "%Y-%m-%d %H:%M")

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
    print(matchedCourseDetails)

# 5.4
def waitingListSizePrediction(cc, ln, ts):
    print("n1, n2, n3, n4, n5")


# 5.5
def  waitingListSizeTraining():
    print("Waiting list size training is successful")








def main():
    courseSearch()

def test():
    temp = datetime.strptime("2018-02-01 15:30", "%Y-%m-%d %H:%M")
    print(temp)

main()
