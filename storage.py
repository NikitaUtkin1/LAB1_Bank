import json
import xml.etree.ElementTree as et
from models.account import Account
from models.savings_account import SavingsAccount
from models.checking_account import CheckingAccount
from models.credit_account import CreditAccount


class Storage:
    @staticmethod
    def save_json(filename, accounts):
        data = []
        for acc in accounts:
            item = {
                "type": type(acc).__name__,
                "number": acc.number,
                "balance": acc.balance
            }
            if type(acc).__name__ == "SavingsAccount":
                item["rate"] = acc.rate
            elif type(acc).__name__ == "CheckingAccount":
                item["limit"] = acc.limit
            elif type(acc).__name__ == "CreditAccount":
                item["credit_limit"] = acc.credit_limit
            data.append(item)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_json(filename):
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)

        accounts = []
        for item in data:
            if item["type"] == "SavingsAccount":
                acc = SavingsAccount(item["number"], item["balance"], item["rate"])
            elif item["type"] == "CheckingAccount":
                acc = CheckingAccount(item["number"], item["balance"], item["limit"])
            elif item["type"] == "CreditAccount":
                acc = CreditAccount(item["number"], item["balance"], item["credit_limit"])
            else:
                acc = Account(item["number"], item["balance"])
            accounts.append(acc)
        return accounts

    @staticmethod
    def save_xml(filename, accounts):
        root = et.Element("Bank")
        for acc in accounts:
            a = et.SubElement(root, "Account", type=type(acc).__name__)
            et.SubElement(a, "Number").text = acc.number
            et.SubElement(a, "Balance").text = str(acc.balance)
            if type(acc).__name__ == "SavingsAccount":
                et.SubElement(a, "Rate").text = str(acc.rate)
            elif type(acc).__name__ == "CheckingAccount":
                et.SubElement(a, "Limit").text = str(acc.limit)
            elif type(acc).__name__ == "CreditAccount":
                et.SubElement(a, "CreditLimit").text = str(acc.credit_limit)

        et.ElementTree(root).write(filename, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def load_xml(filename):
        root = et.parse(filename).getroot()
        accounts = []
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
            accounts.append(acc)
        return accounts