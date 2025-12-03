from pydantic import BaseModel


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    relatedAccountId: int
    timestamp: str