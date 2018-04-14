from operator import itemgetter
from datetime import datetime

# offerings = {cid : [courseDetails]}
# sectionDetails = [Section Num, DateTime, Room, Instructor, Quota, Enrol, Avail, Wait, Remarks]
# courseDetails = [CourseCode, Course Title, Credits, [Pre-re(Course Code)], [Exclusion(Course Code], Course Descr, [[sectionDetails](s)]]

class Course():
    def __init__(self, code, title, credits, prerequisites, exclusions, description, sections):
        self.code = code
        self.credits = credits
        self.prerequisites = prerequisites
        self.exclusions = exclusions
        self.description = description
        self.sections = sections

class Section():
    def __init__(self, section, classNumber, datetime, room ,instructor, quota, enrol, avail, wait , remarks = None):
        #boolean lecture
        self.section = section
        self.classNumber = classNumber
        self.datetime = datetime
        self.room = room
        self.instructor = instructor
        self.quota = quota
        self.enrol = enrol
        self.avail = avail
        self.wait = wait
        self.remarks = remarks
