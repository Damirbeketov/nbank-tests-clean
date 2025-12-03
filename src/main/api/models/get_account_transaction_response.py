from src.main.api.models.base_model import BaseModel

class GetAccountTransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: str
    relatedAccountId: int
