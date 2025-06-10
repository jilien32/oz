from models.user import User

class BankingService:
    # 생성자: 사용자 목록 초기화
    def __init__(self) -> None:
        self.users = []

    # 사용자 추가 메서드
    def add_user(self, username: str) -> None:
        if any(user.username == username for user in self.users):
            raise ValueError("이미 존재하는 사용자입니다.")
        user = User(username)
        self.users.append(user)

    # 사용자 찾기 메서드
    def find_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        raise ValueError("사용자를 찾을 수 없습니다.")

    # 사용자 메뉴 메서드
    def user_menu(self, username: str) -> None:
        user = self.find_user(username)
        while True:
            print("-----------------------------------")
            print(f"사용자: {user.username}, 잔고: {user.account.get_balance()}")
            print("-----------------------------------")
            print("1. 입금")
            print("2. 출금")
            print("3. 거래 내역 조회")
            print("4. 종료")
            choice = input("선택: ")
            
            if choice == '1':
                amount = int(input("입금 금액: "))
                user.account.deposit(amount)
            elif choice == '2':
                amount = int(input("출금 금액: "))
                try:
                    user.account.withdraw(amount)
                except ValueError as e:
                    print(e)
            elif choice == '3':
                transactions = user.account.get_transactions()
                for transaction in transactions:
                    print(transaction)
            elif choice == '4':
                break
            else:
                print("잘못된 선택입니다.")