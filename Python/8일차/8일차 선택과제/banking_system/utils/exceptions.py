# 잔고 부족 예외 클래스
class InsufficientFundsError(Exception):
    def __init__(self, balance: str) -> None:
        super().__init__(balance) + " 잔고가 부족합니다."

# 음수 금액 입력 예외 클래스
class NegativeAmountError(Exception):
    def __init__(self) -> None:
        super().__init__("거래 금액은 음수일 수 없습니다.")

# 사용자 찾기 실패 예외 클래스
class UserNotFoundError(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(username) + " 사용자를 찾을 수 없습니다."