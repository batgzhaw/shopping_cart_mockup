from typing import Optional

from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    name: str = Field(index=True, description="Name of the item")
    quantity: int = Field(description="Quantity of the item to purchase (must be greater than 0)")


class Item(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)
    reservation_id: Optional[int] = None



