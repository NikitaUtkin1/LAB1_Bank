from exceptions import NoMoneyError

class Account:
    def __init__(self, number: str, balance: float = 0) -> None:
        self.number: str = number
        self.balance: float = balance
        self.rate = None

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        if amount > self.balance:
            raise NoMoneyError("Недостаточно средств")
        self.balance -= amount