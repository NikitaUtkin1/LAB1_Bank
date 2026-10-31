from models.account import Account
from exceptions import NoMoneyError

class CheckingAccount(Account):
    def __init__(self, number, balance=0, limit=100):
        super().__init__(number, balance)
        self.limit = limit

    def withdraw(self, amount):
        if amount > self.balance + self.limit:
            raise NoMoneyError("Превышен лимит овердрафта")
        self.balance -= amount