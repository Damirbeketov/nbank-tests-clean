from src.main.api.models.base_model import BaseModel
from typing import Optional, List

class ProfileGetResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    role: str
    accounts: List[object]