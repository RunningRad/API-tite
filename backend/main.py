from fastapi import FastAPI
from utils import get_response
from fastapi.middleware.cors import CORSMiddleware
import json
import glob

app = FastAPI()


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Specify the folder path and file pattern
files = glob.glob('backend/Stores/*.json')
restaurants = []

# Loop through all matching files
for f in files:
    with open(f, 'r') as json_file: 
        restaurant = json.load(json_file)
    restaurants.append(restaurant)



@app.get("/ask")
def read_item(q: str):
    print(f"received query with q: {q}")
    openai_response = get_response(q)
    #return {"text": openai_response}
    return 