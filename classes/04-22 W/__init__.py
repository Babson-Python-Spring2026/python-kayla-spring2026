import json
class Student:
    def __init__(self, name, student_id = None):
        self.name = name
        self.student_id = student_id

class School:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):

        max_id = 0
        for s in self.students:
            if s.student_id != None:
                if s.student_id > max_id:
                    max_id = s.student_id

        student.student_id = max_id + 1

        self.students.append(student)
class Schools:
    def __init__(self):
        self.school = []

    def add_school(self, school):
        self.school.append(school)

mySchools = Schools()

babson = School ('Babson')
mit = School ('MIT')

mySchools.add_school(babson)
mySchools.add_school(mit)

eve = Student('Eve', 1)

babson.add_student(eve)

'''
with open("schools.json", "w") as f:
    json.dump(mySchools, f, indent = 2)
'''
for school in mySchools.school: 

    for student in school.students:
        print(student.name, student.student_id)

