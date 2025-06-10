from models.transaction import Transaction

class Account:
    # 생성자: 잔고와 거래 내역 초기화
    def __init__(self) -> None:
        self.balance = 0
        self.transactions = []

    # 입금 메서드
    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("입금 금액은 0보다 커야 합니다.")
        self.balance += amount
        transaction = Transaction("입금", amount, self.balance)
        self.transactions.append(transaction)

    # 출금 메서드
    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("출금 금액은 0보다 커야 합니다.")
        if amount > self.balance:
            raise ValueError("잔고가 부족합니다.")
        self.balance -= amount
        transaction = Transaction("출금", amount, self.balance)
        self.transactions.append(transaction)

    # 잔고 반환 메서드
    def get_balance(self) -> int:
        return self.balance

    # 거래 내역 반환 메서드
    def get_transactions(self) -> list:
        return [str(transaction) for transaction in self.transactions]
    # 클래스 메서드: 은행 이름 반환
    @classmethod
    def get_bank_name(cls) -> str:
        return "한국은행"

    # 클래스 메서드: 은행 이름 설정
    @classmethod
    def set_bank_name(cls, name: str) -> None:
        cls.bank_name = name