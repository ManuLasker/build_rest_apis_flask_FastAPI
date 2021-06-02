from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request


app = FastAPI(title="RestFul API course",
              description="Api for stores, items and users created for learning purposes")

templates = Jinja2Templates("templates")


@app.get("/", response_class=HTMLResponse)
def index(request:Request):
    print(vars(request))
    return templates.TemplateResponse("index.html", context={"request": request})