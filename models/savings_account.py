from models.account import Account

class SavingsAccount(Account):
    def __init__(self, number, balance=0, rate=0.05):
        super().__init__(number, balance)
        self.rate = rate

    def add_interest(self):
        self.balance += self.balance * self.rate