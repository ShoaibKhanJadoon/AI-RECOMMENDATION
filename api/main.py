from fastapi import FastAPI,Query
from pydantic import BaseModel
from functions import keyword_search
from functions import main_function_recommendation
from typing import List,Optional
from dotenv import load_dotenv
from urllib.parse import urlencode
from data_fetching import Fetch_Data
from preprocessing import get_processed_data
from functions import id_based_recommendations
import os
from fastapi.middleware.cors import CORSMiddleware
import requests
# Load the .env file
load_dotenv()

# Get environment variables
BACKEND_URL = os.getenv("BACKEND_URL")

app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now; you can restrict to specific domains.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.).
    allow_headers=["*"],  # Allow all headers.
)

class ItemRequest(BaseModel):
    item_ids: List[str]

@app.get("/api/{store_id}/search")
def read_root(
    store_id:str, 
    q: str, 
    colorId: Optional[str] = Query(None),
    sizeId: Optional[str] = Query(None)):
    base_url = f"{BACKEND_URL}{store_id}/products"

    query_params = {
        "colorId": colorId,
        "sizeId": sizeId,
    }
    
    # Remove keys with None values
    filtered_params = {k: v for k, v in query_params.items() if v is not None}
    
    
    response = requests.get(base_url, params=filtered_params)
    fetched_data = response.json()

    if not fetched_data:
        return {"result": None}
    processed_data = get_processed_data(fetched_data)

    data = keyword_search(processed_data,q)

    data = data.drop(columns=["tags"])
    return {"result":data.to_dict(orient="records")}

@app.get("/api/{storeId}/products/{productId}")
def read_root(
    productId:str,
    storeId:str
    ):
     
    base_url = f"{BACKEND_URL}{storeId}/products"
    
    fetched_data = Fetch_Data(base_url)

    processed_data = get_processed_data(fetched_data)

    data = id_based_recommendations(processed_data,productId,40)
    
    data = data[data["id"] != productId]

    data = data.drop(columns=["tags"])
    
    return {"result":data.to_dict(orient="records")}
    


@app.post("/api/{store_id}/products")
def read_item(store_id:str, request: ItemRequest,colorId: Optional[str] = Query(None),
    sizeId: Optional[str] = Query(None)):

    base_url = f"{BACKEND_URL}{store_id}/products"
    
    query_params = {
        "colorId": colorId,
        "sizeId": sizeId,
    }
    
    # Remove keys with None values
    filtered_params = {k: v for k, v in query_params.items() if v is not None}
    
    
    response = requests.get(base_url, params=filtered_params)
    fetched_data = response.json()
    
    if not fetched_data:
        return {"result": None}
    if not request.item_ids:
        return {"result": fetched_data}  

    processed_data = get_processed_data(fetched_data)
    
    data = main_function_recommendation(processed_data,request.item_ids)
    data = data.drop(columns=["tags"])
    return {"result":data.to_dict(orient="records")}