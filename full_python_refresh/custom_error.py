class TooManyPagesReadError(ValueError):
    pass

class Book:
    def __init__(self, name: str, page_count:str) -> None:
        self.name = name
        self.page_count = page_count
        self.pages_read = 0
        
    def __repr__(self) -> str:
        return (
            f"<Book {self.name}, read {self.pages_read} pages out of {self.page_count}>"
        )
        
    def read(self, pages: int):
        if self.pages_read + pages > self.page_count:
            raise TooManyPagesReadError(
                f"You tried to read {self.pages_read + pages} pages, but this book only" 
                f"has {self.page_count} pages"
            )
        self.pages_read += pages
        print(f"You have now read {self.pages_read} pages out of {self.page_count}")

book = Book("Harry Potter", 100)
try:
    book.read(140)
except Exception as e:
    print(e)