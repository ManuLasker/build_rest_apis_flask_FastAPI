# Udemy build rest apis with flask course

build rest apis with flask course, this course contains flask for api development, security JWT authentication,
crud apis, and sqlalchemy development to use databases as ORM (Object-relational Mappers).

Learned Frameworks:

- Flask
- Flask-Restful
- Flask-JWT
- Flask-JWT-extended
- Flask-SQLAlchemy
- Sqlite3
- FastAPI

The full dockerized api using Flask ecosystem is located in `sqlalchemy_api_restful` folder. To run this api you need to install docker and docker-compose then execute docker-compose inside the folder specified.

`docker-compose up --build`: this command will build the docker container and run the api using **uWSGI**.

The full dockerized api using FastAPI ecosystem is located in `sqlalchemy_fastapi` folder. To run this api you need to install docker and docker-compose, then execute docker-compose inside the folder specified.

`docker-compose up --build`: this command will build the docker container and run the api using **Gunicorn**.