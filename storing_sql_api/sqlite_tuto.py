import sqlite3
import os

connection = sqlite3.connect('data.db') # sqlite database connection
cursor = connection.cursor() # cursor allows to select things and retrieve data.
                            # (responsable to execute the queries)

create_table = "CREATE TABLE users (id int, username text, password text)" # sql command
# create table execution
try:
    cursor.execute(create_table)
except:
    pass
# create user
user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# create multiples users
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'asdf')
]
cursor.executemany(insert_query, users)

# select query
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# save changes
connection.commit()

connection.close() # close connection
# os.remove('data.db')