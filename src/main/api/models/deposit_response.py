from src.main.api.models.base_model import BaseModel

class DepositResponse(BaseModel):
    id: int
    balance: float
