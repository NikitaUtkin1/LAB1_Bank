import json
import xml.etree.ElementTree as et

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
    def __init__(self, number: str , balance: float = 0):
        self.number: str = number
        self.balance: float = balance
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

    def add(self, account):
        self.accounts.append(account)

    def find(self, number):
        for account in self.accounts:
            if account.number == number:
                return account
        raise LookupError("Аккаунт не найден")

    def remove(self, number):
        # Удаление счёта
        acc = self.find(number)  # кинет LookupError, если нет
        self.accounts.remove(acc)

    def log(self, account_number, amount, kind):
        self.transactions.append(Transaction(account_number, amount, kind))

    def save_json(self, filename):
        data = []
        for acc in self.accounts:
            item = {"type": type(acc).__name__, "number": acc.number, "balance": acc.balance}
            if type(acc).__name__ == "SavingsAccount":
                item["rate"] = acc.perc
            elif type(acc).__name__ == "CheckingAccount":
                item["limit"] = acc.limit
            elif type(acc).__name__ == "CreditAccount":
                item["credit_limit"] = acc.credit_limit
            data.append(item)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_json(self, filename):
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
        self.accounts = []
        for item in data:
            if item["type"] == "SavingsAccount":
                acc = SavingsAccount(item["number"], item["balance"], item["rate"])
            elif item["type"] == "CheckingAccount":
                acc = CheckingAccount(item["number"], item["balance"], item["limit"])
            elif item["type"] == "CreditAccount":
                acc = CreditAccount(item["number"], item["balance"], item["credit_limit"])
            else:
                acc = Account(item["number"], item["balance"])
            self.accounts.append(acc)

    # --- XML ---
    def save_xml(self, filename):
        root = et.Element("Bank")
        for acc in self.accounts:
            a = et.SubElement(root, "Account", type=type(acc).__name__)
            et.SubElement(a, "Number").text = acc.number
            et.SubElement(a, "Balance").text = str(acc.balance)
            if isinstance(acc, SavingsAccount):
                et.SubElement(a, "Rate").text = str(acc.perc)
            if isinstance(acc, CheckingAccount):
                et.SubElement(a, "Limit").text = str(acc.limit)
            if isinstance(acc, CreditAccount):
                et.SubElement(a, "CreditLimit").text = str(acc.credit_limit)
        et.ElementTree(root).write(filename, encoding="utf-8", xml_declaration=True)

    def load_xml(self, filename):
        root = et.parse(filename).getroot()
        self.accounts = []
        for a in root.findall("Account"):
            t = a.get("type")
            num = a.find("Number").text
            bal = float(a.find("Balance").text)
            if t == "SavingsAccount":
                acc = SavingsAccount(num, bal, float(a.find("Rate").text))
            elif t == "CheckingAccount":
                acc = CheckingAccount(num, bal, float(a.find("Limit").text))
            elif t == "CreditAccount":
                acc = CreditAccount(num, bal, float(a.find("CreditLimit").text))
            else:
                acc = Account(num, bal)
            self.accounts.append(acc)


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
    try:
        bank.find("CR1").withdraw(999999)  # сработает NoMoneyError
    except NoMoneyError as e:
        print("Кредитный счёт:", e)

    print("Транзакций:", len(bank.transactions))

    # Демонстрация Delete из CRUD
    bank.add(Account("TEMP1", 50))
    print("Счетов до удаления:", len(bank.accounts))
    bank.remove("TEMP1")
    print("Счетов после удаления:", len(bank.accounts))

    # Сохранение
    bank.save_json("bank.json")
    bank.save_xml("bank.xml")
    print("Данные сохранены в bank.json и bank.xml")

    # Загрузка
    new_bank = Bank()
    new_bank.load_json("bank.json")
    print("Загружено из JSON:", len(new_bank.accounts))

    new_bank2 = Bank()
    new_bank2.load_xml("bank.xml")
    print("Загружено из XML:", len(new_bank2.accounts))
