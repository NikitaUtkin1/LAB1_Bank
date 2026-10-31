from models.client import Client
from models.transaction import Transaction
from exceptions import NoMoneyError


class Bank:
    def __init__(self):
        self.accounts = []
        self.transactions = []

    def add(self, account):
        self.accounts.append(account)

    def find(self, number):
        for acc in self.accounts:
            if acc.number == number:
                return acc
        raise LookupError("Счёт не найден")

    def remove(self, number):
        acc = self.find(number)
        self.accounts.remove(acc)

    def log(self, account_number, amount, kind):
        self.transactions.append(Transaction(account_number, amount, kind))

    def transfer(self, from_number, to_number, amount):
        sender = self.find(from_number)
        receiver = self.find(to_number)

        if amount > sender.balance:
            raise NoMoneyError(f"Недостаточно средств для перевода. Баланс: {sender.balance}")

        sender.withdraw(amount)
        receiver.deposit(amount)

        self.log(from_number, amount, "transfer_out")
        self.log(to_number, amount, "transfer_in")

        return f"Перевод {amount} руб. выполнен с {from_number} на {to_number}."