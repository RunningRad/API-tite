from fastapi import FastAPI
from quin import getStoreRecommendations
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
#from test-app import create_delivery
#from delivery_update import get_update
=======
from delivery_update import get_update
from test-app import create_delivery
>>>>>>> 5523f6e66888fea030bdd1ae8101ef74ca36112c

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

# @app.get("/send")
# def create(store, place):
#     print(f"received query with store: {store}, place: {place}")
#     id = create_delivery(store, place)
#     return {"text": "Delivery created", "Delivery_id": id}

# @app.get("/update")
# def update():
#     print(f"request for update received")
#     status = get_update(q)
#     return {"text": "update", "staus": status}
