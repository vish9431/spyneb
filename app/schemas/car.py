from pydantic import BaseModel
from typing import List, Optional

class CarBase(BaseModel):
    title: str
    description: str
    car_type: str
    company: str
    dealer: str
    images: List[str]

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    pass

class Car(CarBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True