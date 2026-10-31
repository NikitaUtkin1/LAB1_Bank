class Transaction:
    def __init__(self, account_number, amount, kind):
        self.account_number = account_number
        self.amount = amount
        self.kind = kind  # "deposit" или "withdraw"