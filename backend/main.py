from fastapi import FastAPI
from quin import getStoreRecommendations
from fastapi.middleware.cors import CORSMiddleware


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

@app.get("/ask")
def read_item(q: str):
    print(f"received query with q: {q}")
    openai_response = getStoreRecommendations(q)
    return {"text": "Here is what i could find for you", "store_options": openai_response}
