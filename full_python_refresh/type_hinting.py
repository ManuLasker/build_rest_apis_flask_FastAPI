from typing import List


def list_avg(sequence: List) -> float:
    return sum(sequence)/len(sequence)


class Book:
    pass


class BookShelf:
    def __init__(self, books: List[Book]):
        self.books = books


list_avg(10)
