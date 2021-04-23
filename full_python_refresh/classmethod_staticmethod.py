class ClassTest:
    
    def instance_method(self): # to change something inside the instance
        print(f"Called instance_method of {self}")
        
    @classmethod # factories
    def class_method(cls):
        print(f"called class_method of {cls}")
        
    @staticmethod # to put a method inside the class does not use the class or anything
    def static_method():
        print("Called static_method.")
        
test = ClassTest()
test.instance_method()
ClassTest.class_method()
ClassTest.static_method()


# Factories
class Book:
    TYPES = ("hardcover", "paperback")
    
    def __init__(self, name, book_type, weight) -> None:
        self.name = name
        self.book_type = book_type
        self.weight = weight
    
    def __repr__(self) -> str:
        return f"<Book {self.name}, {self.book_type}, {self.weight}g>"
    
    @classmethod
    def hardcover(cls, name, page_weight):
        return cls(name, cls.TYPES[0], page_weight + 100)
    
    @classmethod
    def paperback(cls, name, page_weight):
        return cls(name, cls.TYPES[1], page_weight - 100)
    
book = Book("Harry Potter", "hardcover", 1500)
book_hardcover = Book.hardcover("Harry Potter", 1500)
book_paperback = Book.paperback("Harry Potter", 1500)
print(book, book_hardcover, book_paperback)
