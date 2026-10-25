class NoMoneyError(Exception):
    pass


class Client:
    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id


class Transaction:
    def __init__(self, account_number, amount, kind):
        self.account_number = account_number
        self.amount = amount
        self.kind = kind  # "deposit" или "withdraw"


class Account:
    def __init__(self, number , balance=0):
        self.name = number
        self.balance = balance
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма не может быть меньше нуля")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма не может быть меньше нуля")
        if amount > self.balance:
            raise NoMoneyError("Недостаточно средств")
        self.balance -= amount


class SavingsAccount(Account):
    def __init__(self, number , balance=0, perc=0.05):
        super().__init__(number , balance)
        self.perc=perc

    def add_interest(self):
        self.balance += self.balance * self.perc


class CheckingAccount(Account):
    def __init__(self, number , balance=0, limit=500):
        super().__init__(number , balance)
        self.limit = limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Превышен лимит")
        self.balance -= amount

class CreditAccount(Account):
    def __init__(self, number, balance=0, credit_limit=1000):
        super().__init__(number, balance)
        self.credit_limit = credit_limit

    def withdraw(self, amount):
        if amount > self.balance + self.credit_limit:
            raise NoMoneyError("Превышен кредитный лимит")
        self.balance -= amount

class Bank:
    def __init__(self):
        self.accounts = []
        self.transactions = []

    def add_account(self, account):
        self.accounts.append(account)

    def find(self, number):
        for account in self.accounts:
            if account.name == number:
                return account
        raise LookupError("Аккаунт не найден")

if __name__ == "__main__":
    bank = Bank()

    client1 = Client("Иван", 1)
    client2 = Client("Мария", 2)
    print("Клиенты:", client1.name, client2.name)

    bank.add(SavingsAccount("S1", 1000, 0.5))
    bank.add(CheckingAccount("C1", 500, 200))
    bank.add(CreditAccount("CR1", 0, 5000))

    try:
        bank.find("S1").withdraw(300)
        bank.log("S1", 300, "withdraw")
        bank.find("C1").deposit(100)
        bank.log("C1", 100, "deposit")
        bank.find("S1").withdraw(123456)  # сработает NoMoneyError
    except NoMoneyError as e:
        print("Свое исключение",e)
    except LookupError as e:
        print("Не найден счет",e)
    except ValueError as e:
        print("Сумма указана неверно",e)

