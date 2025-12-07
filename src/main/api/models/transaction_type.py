from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"