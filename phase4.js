db = db.getSiblingDB("courses");


db.course2.aggregate(
[
	{$unwind:"$TimeList"},
	{$project:{_id:0,Cname:1,TimeList:1}},
	{$unwind:"$TimeList.SectionList"},
	{$project:{
		_id:0,
		Cname:1,
		"TimeList.timeslot":1,
		"TimeList.SectionList.section":1,
		"TimeList.SectionList.date_time":1,
		"TimeList.SectionList.quota":1,
		"TimeList.SectionList.enrol":1,
		"TimeList.SectionList.available":1,
		"TimeList.SectionList.wait":1,
		"fenrol":{$multiply:[0.05,1]}}},
	{$project:{
		_id:0,
		Cname:1,
		"TimeList.timeslot":1,
		"TimeList.SectionList.section":1,
		"TimeList.SectionList.date_time":1,
		"TimeList.SectionList.quota":1,
		"TimeList.SectionList.enrol":1,
		"TimeList.SectionList.available":1,
		"TimeList.SectionList.wait":1,
		"fenrol":1,
		"TimeList.SectionList.Satisfied":{
			$cond:{
				if:{
					$gte: ["$TimeList.SectionList.wait", "$fenrol"]
				},
				then: "Yes",
				else: "No",
			}
		}
	}},
	{$project:{
		_id:0,
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
	{$group:{
		"_id":{
			"Cname":"$Cname",
			"timeslot":"$timeslot"
		},
		"List":{$push:{"List":"$List"}}

	}},
	{$project:{
		_id:0,
		"Cname":"$_id.Cname",
		"timeslot":"$_id.timeslot",
		"List":"$List.List"
		
	}},
	{$out:"allWithStatisfied"}
]
)

cursor=db.course.aggregate(
[
	{$unwind:"$TimeList"},
	//match the timeslot(Date object) twice to filter out only the time within the range using the gte and lte operations
	{$project: {Course_Code:1, Cname:1, Units:1, _id:0, TimeList:1, greater_than_start: {$gte: ["$TimeList.timeslot", new Date("2018-02-01T11:00:00Z")]} ,less_than_end: {$lte: ["$TimeList.timeslot", new Date("2018-02-10T12:00:00Z")]}}},
	{$match: {greater_than_start:true}},
	{$match: {less_than_end:true}},
	{$unwind:"$TimeList.SectionList"},
	//match only the section of object is Lecture using regular expression, as required
	{$match: {"TimeList.SectionList.section":/^L/i}},
	//would match again to keep only the section that match the waitlist requirement (i.e. the number of students in the waiting list of this lecture section is greater than or equal to f multiplied by the number of students enrolled in this lecture section in that time slot.)
	//The initial value of f is hardcoded as 0.05.
	{$project: {Course_Code:1, Cname:1, Units:1, _id:0, TimeList:1, wait_list_fulfilled: {$gte: ["$TimeList.SectionList.wait", 0.05*"$TimeList.SectionList.enrol"]}}},
	{$match: {wait_list_fulfilled:true}},
	//to retrieve the most updated information, we order it in descedning order; the $first operation can get the most updated info
	//$first is a feature that returns the value that results from applying an expression to the first document in a group of documents that share the same group by key. Only meaningful when documents are in a defined order.
	{$sort:{Cname:-1,"TimeList.timeslot":-1}},
	{$group:{
		"_id": "$Course_Code",
		"CourseTitle": {"$first": "$Cname"},
		"NoOfUnits": {"$first": "$Units"},
		"MatchedTimeSlot": {"$first": "$TimeList.timeslot"}		
		}
	},
	//lookup the information of the course_section that fulfill the waitlist requirement from the "All" document we outputted at the beginning
	//used a complicated operation, joining them using two attributes i.e. course name and timeslot. 
	{$lookup:
		{
			from: "allWithStatisfied",
			let:{time:"$MatchedTimeSlot",name:"$CourseTitle"},
			pipeline:[
				{$match:
					{$expr:
						{$and:
							[
							{$eq:["$Cname", "$$name"]},
							{$eq:["$timeslot", "$$time"]}
							]
						}
					}
				}
				],
			as: "course_info"
		}
	},
	//output the information as required
	{$project:{_id:1,CourseTitle:1,NoOfUnits:1,MatchedTimeSlot:1,SectionList:"$course_info.List"}},
	{$project:{_id:1,CourseTitle:1,NoOfUnits:1,MatchedTimeSlot:1,"SectionList.section":1,"SectionList.date_time":1,"SectionList.quota":1,"SectionList.enrol":1,"SectionList.available":1,"SectionList.wait":1,"SectionList.Satisfied":1}}
]
)


while ( cursor.hasNext() ) {
   printjson( cursor.next() );
}