import random
import time
from typing import List

import httpx
import uvicorn
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlmodel import Session, select, SQLModel

from app.db import SessionLocal, engine
from app.models import Item, ItemBase


class LazyDbInit:
    """
    Create the db schema, just once.
    """
    is_initizalized = False

    @classmethod
    def initialize(cls):
        if not cls.is_initizalized:
            SQLModel.metadata.create_all(engine)
            cls.is_initizalized = True


server = FastAPI()


# Dependency
def get_db():
    # Create the db schema, if needed, before starting a session.
    # This is a workaround for an issue where the FastAPI server
    # may be started before the Postgresql db is ready.
    # I didn't manage to solve this in the docker-compose compose.yml file.
    # The healtcheck configuration doesn't seem to work.
    LazyDbInit.initialize()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@server.post("/reserve")
async def reservation_mockup(item: Item):
    """ Mockup of the reservation API endpoint to make the code runnable. """
    time.sleep(20)
    print("reservation mockup finished")
    return {'reservation_id': random.randint(1, 10000)}


async def call_reservation_api(item: Item):
    """Background task to call the external reservation API."""
    url = "http://127.0.0.1:8000/reserve"  # Replace with the actual API URL
    print(url)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=item.model_dump())
            response.raise_for_status()
        except Exception as e:
            # Handle exceptions if needed
            print("Error during external API call:", e)


@server.post("/items", response_model=Item)
async def add_item(order: ItemBase, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """ Endpoint to add items to the database (shopping cart). """
    if order.quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity must be greater than 0")
    db_item = Item.model_validate(order)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    background_tasks.add_task(call_reservation_api, order)
    return db_item


@server.get("/items", response_model=List[ItemBase])
async def get_item_list(db: Session = Depends(get_db)):
    """ Endpoint to get all items from the database (shopping cart). """
    return db.exec(select(Item)).all()


if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8001)
