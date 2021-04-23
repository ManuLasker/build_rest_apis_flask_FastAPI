class Student:
    def __init__(self, name, grades) -> None:
        self.name = name
        self.grades = grades
    
    @property
    def average(self):
        return sum(self.grades)/len(self.grades)
    
student = Student(name="Rolf", grades=(100, 90, 80))
print(student.average)