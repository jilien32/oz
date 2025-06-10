from services.banking_service import BankingService

def main() -> None:
    # BankingService 인스턴스 생성
    # 사용자 입력을 받아 사용자 추가 및 찾기 기능 구현
    # 사용자 메뉴를 통해 입금, 출금, 잔고 확인, 거래 내역 기능을 제공
    # 여기에 코드를 작성하세요
    banking_service = BankingService()
    while True:
        print("1. 사용자 추가")
        print("2. 사용자 찾기")
        print("3. 종료")
        choice = input("선택: ")
        
        if choice == '1':
            username = input("사용자 이름: ")
            try:
                banking_service.add_user(username)
                print(f"{username} 사용자가 추가되었습니다.")
            except ValueError as e:
                print(e)
        elif choice == '2':
            username = input("사용자 이름: ")
            try:
                banking_service.user_menu(username)
            except ValueError as e:
                print(e)
        elif choice == '3':
            break
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()