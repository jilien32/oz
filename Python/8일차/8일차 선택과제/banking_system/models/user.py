from models.account import Account

class User:
    #  생성자: 사용자 이름과 계좌 초기화
    def __init__(self, username: str) -> None:
        self.username = username
        self.account = Account()
        self.bank_name = Account.get_bank_name()