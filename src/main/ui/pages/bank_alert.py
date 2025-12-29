from enum import Enum


class BankAlert(str, Enum):
    USER_CREATED_SUCCESSFULLY = "✅ User created successfully!"
    USERNAME_MUST_BE_BETWEEN_3_AND_15_CHARACTERS = "Username must be between 3 and 15 characters"
    NEW_ACCOUNT_CREATED = "✅ New Account Created! Account Number: "
    DEPOSIT_MONEY_ACCOUNT = f"✅ Successfully deposited"
    DEPOSIT_MONEY_NEGATIVE_ACCOUNT = f"❌ Please deposit less or equal to 5000$."
    TRANSFER_SUCCESS = f"✅ Successfully transferred $"
    TRANSFER_INVALID = f"❌ Error: Invalid transfer: insufficient funds or invalid accounts"
    CONFIRM_CHECK = f"❌ Please fill all fields and confirm."
    NO_USER_FOUND = f"❌ No user found with this account number."
    TRANSFER_SUCCESS_OUT = f"Transfer of $.* successful"
    EDIT_PROFILE_SUCCESS = f"✅ Name updated successfully!"
    NAME_NOT_MATCH = f"❌ The recipient name does not match the registered name."
