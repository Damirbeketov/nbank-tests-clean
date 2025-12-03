from src.main.api.models.base_model import BaseModel

class CustomerProfileResponse(BaseModel):
    id: int
    username: str
    name: str | None
    role: str
    accounts: list