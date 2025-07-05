from datetime import datetime
import random
import string
import re


class Transaction:
    def __init__(self, transaction_type, amount, balance_after, description=""):
        self.transaction_id = self._generate_id()
        self.timestamp = datetime.now()
        self.type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.description = description

    @staticmethod
    def _generate_id():
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"TXN{timestamp}{random_str}"

    def __str__(self):
        return (f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{self.type}: {self.amount:,}원 (잔액: {self.balance_after:,}원)")

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'timestamp': self.timestamp.isoformat(),
            'type': self.type,
            'amount': self.amount,
            'balance_after': self.balance_after,
            'description': self.description
        }


class Account:
    bank_name = "파이썬 은행"
    total_accounts = 0
    total_balance = 0
    accounts_type = {}

    def __init__(self, account_number, owner_name, initial_balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.__balance = initial_balance
        self.is_active = True
        self.created_at = datetime.now()
        self.__transactions = []

        Account.total_accounts += 1
        Account.total_balance += initial_balance

        account_type = self.__class__.__name__
        Account.accounts_type[account_type] = Account.accounts_type.get(account_type, 0) + 1

        if initial_balance > 0:
            self.__transactions.append(Transaction("deposit", initial_balance, initial_balance, "계좌 개설 초기 입금"))

    @property
    def balance(self):
        return self.__balance

    @property
    def transaction_count(self):
        return len(self.__transactions)

    def deposit(self, amount):
        if not self.is_active:
            raise ValueError("비활성화된 계좌입니다.")
        if amount <= 0:
            raise ValueError("입금액은 0보다 커야합니다.")

        self.__balance += amount
        Account.total_balance += amount
        self.__transactions.append(Transaction("deposit", amount, self.__balance))
        return True, f"{amount:,}원이 입금되었습니다. (잔액: {self.__balance:,}원)"

    def withdraw(self, amount):
        if not self.is_active:
            raise ValueError("비활성화된 계좌입니다.")
        if amount <= 0:
            raise ValueError("출금액은 0보다 커야합니다.")
        if amount > self.__balance:
            raise ValueError(f"잔액이 부족합니다. (현재 잔액: {self.__balance:,}원)")

        self.__balance -= amount
        Account.total_balance -= amount
        self.__transactions.append(Transaction("withdrawal", amount, self.__balance))
        return True, f"{amount:,}원이 출금되었습니다. (잔액: {self.__balance:,}원)"

    def transfer(self, target_account, amount):
        if not isinstance(target_account, Account):
            raise TypeError("유효한 계좌가 아닙니다.")
        if target_account == self:
            raise ValueError("같은 계좌로는 이체할 수 없습니다.")

        try:
            self.withdraw(amount)
            target_account.deposit(amount)

            self.__transactions[-1].type = "transfer_out"
            self.__transactions[-1].description = f">> {target_account.account_number}"
            target_account.__transactions[-1].type = "transfer_in"
            target_account.__transactions[-1].description = f"<< {self.account_number}"

            return True, f"{amount:,}원을 {target_account.account_number}로 이체했습니다."
        except Exception as e:
            self.__balance += amount
            Account.total_balance += amount
            if self.__transactions:
                self.__transactions.pop()
            raise e

    def get_transactions(self, limit=None, transaction_type=None):
        transactions = self.__transactions.copy()
        if transaction_type:
            transactions = [t for t in transactions if t.type == transaction_type]
        transactions.reverse()
        return transactions[:limit] if limit else transactions

    def get_account_summary(self):
        return {
            'account_number': self.account_number,
            'owner_name': self.owner_name,
            'balance': self.__balance,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'transaction_count': len(self.__transactions),
            'account_type': self.__class__.__name__
        }

    def close_account(self):
        if self.__balance > 0:
            raise ValueError(f"잔액이 있는 계좌는 폐쇄할 수 없습니다. (잔액: {self.__balance:,}원)")
        self.is_active = False
        Account.total_accounts -= 1
        Account.accounts_type[self.__class__.__name__] -= 1
        return True, "계좌가 폐쇄되었습니다."

    @classmethod
    def get_bank_statistics(cls):
        return {
            'bank_name': cls.bank_name,
            'total_accounts': cls.total_accounts,
            'total_balance': cls.total_balance,
            'average_balance': cls.total_balance / cls.total_accounts if cls.total_accounts > 0 else 0,
            'account_types': dict(cls.accounts_type)
        }

    @classmethod
    def generate_account_number(cls):
        timestamp = datetime.now().strftime('%Y%m%d')
        random_digits = ''.join(random.choices(string.digits, k=6))
        return f"{timestamp}-{random_digits}"

    @staticmethod
    def validate_account_number(account_number):
        return re.match(r'^\d{8}-\d{6}$', account_number) is not None

    @staticmethod
    def format_currency(amount):
        return f"{amount:,.0f}원"

    def __str__(self):
        return (f"{self.__class__.__name__} - {self.account_number}\n"
                f"예금주: {self.owner_name}\n"
                f"잔액: {self.format_currency(self.__balance)}")

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.account_number}', '{self.owner_name}', {self.__balance})"

class SavingsAccount(Account):
    def __init__(self, account_number, owner_name, interest_rate, initial_balance=0):
        super().__init__(account_number, owner_name, initial_balance)
        self.interest_rate = interest_rate  # 연 이율 (%)
        self.last_interest_date = datetime.now()
        self.minimum_balance = 10000  # 최소 잔액

    def add_monthly_interest(self):
        days_passed = (datetime.now() - self.last_interest_date).days

        if days_passed < 30:
            return False, f"이자 지급일이 아닙니다. ({30 - days_passed}일 후 지급)"

        monthly_rate = self.interest_rate / 12 / 100
        interest = int(self.balance * monthly_rate)

        if interest > 0:
            self._Account__balance += interest
            Account.total_balance += interest

            transaction = Transaction(
                "interest", interest, self._Account__balance,
                f"월 이자 지급 (연 {self.interest_rate}%)"
            )
            self._Account__transactions.append(transaction)

            self.last_interest_date = datetime.now()
            return True, f"이자 {interest:,}원이 지급되었습니다."

        return False, "이자가 0원입니다."

    def withdraw(self, amount):
        if self.balance - amount < self.minimum_balance:
            raise ValueError(f"최소 잔액 {self.minimum_balance:,}원을 유지해야 합니다.")
        return super().withdraw(amount)

def demo_bank_system():
    print("=== 파이썬 은행 시스템 데모 ===\n")

    print("1. 계좌 생성")
    savings1 = SavingsAccount(Account.generate_account_number(), "김철수", interest_rate=3.5, initial_balance=2000000)
    savings2 = SavingsAccount(Account.generate_account_number(), "김영희", interest_rate=3.5, initial_balance=2000000)
    print(f"저축 계좌 생성 완료: {savings1.account_number}")
    print(f"저축 계좌 생성 완료: {savings2.account_number}")

    print("\n" + "-"*50 + "\n")

    print("2. 거래 실행")
    success, msg = savings1.transfer(savings2, 500000)
    print(f"이체: {msg}")

    print("\n" + "-"*50 + "\n")

    print("3. 이자 처리")
    savings1.last_interest_date = datetime.now() - timedelta(days=31)
    success, msg = savings1.add_monthly_interest()
    print(f"저축계좌 1: {msg}")

    savings2.last_interest_date = datetime.now() - timedelta(days=31)
    success, msg = savings2.add_monthly_interest()
    print(f"저축계좌 2: {msg}")

    print("\n" + "-"*50 + "\n")

    print("4. 계좌 정보 조회\n")
    for account in [savings1, savings2]:
        print(account)
        print()

    print("\n" + "-"*50 + "\n")

    print("5. 최근 거래 내역\n")
    for account in [savings1, savings2]:
        print(f"{account.owner_name}님의 거래 내역:")
        for transaction in account.get_transactions(limit=5):
            print(f"   {transaction}")
        print()

    print("\n" + "-"*50 + "\n")

    print("6. 은행 전체 통계\n")
    stats = Account.get_bank_statistics()
    print(f"은행명: {stats['bank_name']}")
    print(f"총 계좌 수: {stats['total_accounts']}")
    print(f"총 예치금: {stats['total_balance']:,.0f}원")
    print(f"평균 잔액: {stats['average_balance']:,.0f}원")
    print(f"계좌 유형별: {stats['account_types']}")

if __name__ == "__main__":
    from datetime import timedelta
    demo_bank_system()