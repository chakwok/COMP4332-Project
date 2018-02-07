URL = None
courses = ["COMP4332" , "ELEC1010", "COMP3221", "Big Data Management", "Dumb Data", "sth"]


# 5.1
def dropAndEmptySuccessful():
    print("Collection dropping and empty collection creating are successful")

# 5.2
def crawlData(enteredURL):
    if (URL == "default"):
        print("Data Crawling is successful and all data are inserted into the database")
    else:
        url = enteredURL
        print("Data Crawling is successful and all data are inserted into the database")

# 5.3
def courseSearch():
    print("There are two search operations available:")
    print("\t1. Course Search by Keyword")
    print("\t2. Course Search by Waiting List Size\n")
    choice = input("Please indicata the preferred operation\n")

    matchedCourses = []
    if choice == "1":
        query = input("Please enter your keyword\n")
        keywords = query.split()
        for keyword in keywords:
            for course in courses:
                if (course.find(keyword) != -1 ):
                    matchedCourses.append(course)
    elif choice == "2":
        #search
        print("sth")
    else:
        print("Please enter a valid choice\n")

    printAllCourses(matchedCourses)

def printAllCourses(courses):
    if courses == None:
        print("There is no match")
    else:
        print("Here is all the matched courses")
        for course in courses:
            print(course)

def main():
    courseSearch()

main()
