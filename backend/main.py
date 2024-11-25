from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from quin import getStoreRecommendations
from test_app import create_delivery
from delivery_update import get_update

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

# Define a Pydantic model for the delivery request
class DeliveryRequest(BaseModel):
    storeName: str
    address: str
    orderValue: float

@app.get("/ask")
def read_item(q: str):
    print(f"received query with q: {q}")
    openai_response = getStoreRecommendations(q)
    return {"text": "Here is what I could find for you", "store_options": openai_response}

@app.post("/create-delivery")
def create_delivery_endpoint(delivery: DeliveryRequest):
    print(f"received delivery request: {delivery}")
    try:
        id = create_delivery(delivery.storeName, delivery.address, delivery.orderValue)
        return {"text": "Delivery created", "delivery_id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/update")
def update(q: str):  # Accept a query parameter
    print(f"Request for update received with query: {q}")
    status = get_update()
    return {"text": "update", "status": status}
