from src.main.api.models.base_model import BaseModel

class TransferResponse(BaseModel):
    senderAccountId: int
    message: str
    amount: float
    receiverAccountId: int
