from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="RestFul API course",
              description="Api for stores, items and users"
              " created for learning purposes")

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
