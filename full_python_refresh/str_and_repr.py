class Person:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
        
    def __str__(self) -> str:
        return f'Person {self.name}, {self.age} years old'
    
    def __repr__(self) -> str:
        return f'<Person({self.name}, {self.age})>'

bob = Person("Bob", 25)
print(bob)
print(bob.__repr__()) # use in debugger
