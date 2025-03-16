from enum import Enum


class AssetTypeEnum(Enum):

    CASH = "Cash"
    BANK_ACCOUNT = "Bank Account"
    POCKET_MONEY = "Pocket Money"
    INVESTMENT = "Investment"
    REAL_ESTATE = "Real Estate"
    OTHER = "Other"


class TransactionTypeEnum(Enum):

    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
