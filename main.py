from models.account import Account
from models.savings_account import SavingsAccount
from models.checking_account import CheckingAccount
from models.credit_account import CreditAccount
from models.client import Client
from exceptions import NoMoneyError
from bank import Bank
from storage import Storage

if __name__ == "__main__":
    bank = Bank()

    client1 = Client("Иван", 1)
    client2 = Client("Мария", 2)
    print("Клиенты:", client1.name, client2.name)

    bank.add(SavingsAccount("S1", 1000, 0.1))
    bank.add(CheckingAccount("C1", 500, 200))
    bank.add(CreditAccount("CR1", 0, 5000))

    try:
        bank.find("S1").withdraw(300)
        bank.log("S1", 300, "withdraw")

        bank.find("C1").deposit(100)
        bank.log("C1", 100, "deposit")

        bank.find("S1").withdraw(99999)   # сработает NoMoneyError
    except NoMoneyError as e:
        print("Своё исключение:", e)
    except LookupError as e:
        print("Счёт не найден:", e)
    except ValueError as e:
        print("Неверная сумма:", e)

    try:
        bank.find("CR1").withdraw(999999)  # сработает NoMoneyError (кредит)
    except NoMoneyError as e:
        print("Ошибка кредита:", e)

    print("Транзакций:", len(bank.transactions))

    try:
        print("\n ТЕСТ ПЕРЕВОДА ")
        msg = bank.transfer("S1", "C1", 200)
        print(msg)
        print(f"Новый баланс S1: {bank.find('S1').balance}")
        print(f"Новый баланс C1: {bank.find('C1').balance}")
    except NoMoneyError as e:
        print("Ошибка перевода:", e)

    bank.add(Account("TEMP1", 50))
    print("\nСчетов до удаления:", len(bank.accounts))
    bank.remove("TEMP1")
    print("Счетов после удаления:", len(bank.accounts))

    Storage.save_json("data.json", bank.accounts)
    Storage.save_xml("data.xml", bank.accounts)
    print("Данные сохранены в data.json и data.xml")

    new_bank_accounts_json = Storage.load_json("data.json")
    print("Загружено из JSON:", len(new_bank_accounts_json))

    new_bank_accounts_xml = Storage.load_xml("data.xml")
    print("Загружено из XML:", len(new_bank_accounts_xml))