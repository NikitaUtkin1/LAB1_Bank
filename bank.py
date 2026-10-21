class NoMoneyError(Exception):
    pass

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


class Bank:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def find(self, number):
        for account in self.accounts:
            if account.name == number:
                return account
        raise LookupError("Аккаунт не найден")

if __name__ == "__main__":
    bank = Bank()
    bank.add(SavingsAccount("S1", 1000, 0.5))
    bank.add(CheckingAccount("C1", 500, 200))

    try:
        bank.find("S1").withdraw(100)
        bank.find("C1").deposit(200)
        bank.find("S1").withdraw(1234567)
    except NoMoneyError as e:
        print("Свое исключение",e)
    except LookupError as e:
        print("Не найден счет",e)
    except ValueError as e:
        print("Сумма указана неверно",e)

    new_bank = Bank()