from src.main.api.models.base_model import BaseModel
from typing import List

class CustomerProfile(BaseModel):
    id: int
    username: str
    name: str
    role: str
    accounts: List[object]

class ProfileResponse(BaseModel):
    customer: CustomerProfile
    message: str