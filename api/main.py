from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from functions import keyword_search
from functions import main_function_recommendation
from typing import List

app = FastAPI()

class ItemRequest(BaseModel):
    item_ids: List[str]

@app.get("/search")
def read_root(q: Union[str, None] = None):
    data = keyword_search(q)
    data = data.drop(columns=["tags"])
    return {"result":data.to_dict(orient="records")}


@app.post("/items")
def read_item(request: ItemRequest):
    data = main_function_recommendation(request.item_ids)
    return {"result":data.to_dict(orient="records")}