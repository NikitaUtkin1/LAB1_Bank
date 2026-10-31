from models.account import Account
from exceptions import NoMoneyError

class CreditAccount(Account):
    def __init__(self, number, balance=0, credit_limit=1000):
        super().__init__(number, balance)
        self.credit_limit = credit_limit

    def withdraw(self, amount):
        if amount > self.balance + self.credit_limit:
            raise NoMoneyError("Превышен кредитный лимит")
        self.balance -= amount