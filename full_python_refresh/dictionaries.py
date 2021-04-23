student = [{"name":"Jose", "school":"Computing","grades":(66,77,88,)},
           {"name":"Jose", "school":"Computing","grades":(22,77,88,)}]

def average_grade_all_students(student_list):
    sums =[(sum(student["grades"]), len(student["grades"])) for student in student_list]
    total, count = list(zip(*sums)) # unzip
    return sum(total)/sum(count)

print(average_grade_all_students(student))