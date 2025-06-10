class Transaction:
    # 생성자: 거래 유형, 금액, 잔고를 초기화
    def __init__(self, transaction_type: str, amount: int, balance: int) -> None:
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance = balance

    # 거래 정보를 문자열로 반환하는 메서드
    def __str__(self) -> str:
        return f"{self.transaction_type} {self.amount} {self.balance}"

    # 거래 정보를 튜플로 반환하는 메서드
    def to_tuple(self) -> tuple:
        return (self.transaction_type, self.amount, self.balance)