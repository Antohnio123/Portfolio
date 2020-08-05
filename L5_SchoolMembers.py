class SchoolMember:
    """A class of whoever, having something common with a school.
    :name: a name of this person.
    :age: an age of this person."""
    def __init__(self, name, age):
        self.Name = name
        self.Age = age

    def show(self):
        """A method, showing all the info about a person."""
        result_string=''
        attributes = self.__dict__
        for k, v in attributes.items():
            result_string += str(k)+': '+str(v)+", "
        result_string=result_string[:-2]
        return result_string


class Teacher(SchoolMember):
    """A class of a teacher, working in a school.
        :name: a name of this teacher.
        :age: an age of this teacher.
        :salary: a monthly salary, that is paid to a teacher"""
    def __init__(self, name, age, salary):
        super().__init__(name=name, age=age)
        self.Salary = salary


class Student(SchoolMember):
    """A class of a student, attending a school.
        :name: a name of this student.
        :age: an age of this student.
        :grades: a total grade of a student, which is usually a summary of all his grades."""
    def __init__(self, name, age, grades):
        super().__init__(name=name, age=age)
        self.Grades = grades


persons = [Teacher("Mr.Poopybutthole", 40, 3000), Student("Morty", 16, 75)]

for person in persons:
    print(person.show())