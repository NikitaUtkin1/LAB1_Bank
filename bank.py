class Account:
def __init__(self, number , balance=0):
        self.name = number
        self.balance = balance

class SavingsAccount(Account):
    def __init__(self, number , balance=0, perc=0.05):
        super().__init__(number , balance)
        self.perc=perc

class CheckingAccount(Account):
    def __init__(self, number , balance=0, limit=500):
        super().__init__(number , balance)
        self.limit = limit

class Bank:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def find(self, number):
        for account in self.accounts:
            if account.name == number:
                return account
        raise LookupError("Account not found")
