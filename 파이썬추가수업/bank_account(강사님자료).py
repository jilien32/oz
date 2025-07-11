from datetime import datetime
import json
import random
import string

class Transaction:
    """거래 내역을 나타내는 클래스"""
    
    def __init__(self, transaction_type, amount, balance_after, description=""):
        self.transaction_id = self._generate_id()
        self.timestamp = datetime.now()
        self.type = transaction_type  # 'deposit', 'withdrawal', 'transfer', 'interest'
        self.amount = amount
        self.balance_after = balance_after
        self.description = description
    
    @staticmethod
    def _generate_id():
        """거래 ID 생성"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"TXN{timestamp}{random_str}"
    
    def __str__(self):
        return (f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{self.type}: {self.amount:,}원 (잔액: {self.balance_after:,}원)")
    
    def to_dict(self):
        """딕셔너리로 변환 (JSON 저장용)"""
        return {
            'transaction_id': self.transaction_id,
            'timestamp': self.timestamp.isoformat(),
            'type': self.type,
            'amount': self.amount,
            'balance_after': self.balance_after,
            'description': self.description
        }

class Account:
    """기본 계좌 클래스"""
    
    # 클래스 변수
    bank_name = "파이썬 은행"
    total_accounts = 0
    total_balance = 0
    account_types = {}
    
    def __init__(self, account_number, owner_name, initial_balance=0):
        # 계좌 기본 정보
        self.account_number = account_number
        self.owner_name = owner_name
        self.__balance = initial_balance  # private 속성
        self.is_active = True
        self.created_at = datetime.now()
        
        # 거래 내역 관리
        self.__transactions = []  # private 속성
        
        # 클래스 변수 업데이트
        Account.total_accounts += 1
        Account.total_balance += initial_balance
        
        # 계좌 타입별 카운트
        account_type = self.__class__.__name__
        Account.account_types[account_type] = Account.account_types.get(account_type, 0) + 1
        
        # 초기 입금 기록
        if initial_balance > 0:
            self.__transactions.append(
                Transaction("deposit", initial_balance, initial_balance, "초기 입금")
            )
    
    @property
    def balance(self):
        """잔액 조회 (읽기 전용)"""
        return self.__balance
    
    @property
    def transaction_count(self):
        """거래 횟수"""
        return len(self.__transactions)
    
    def deposit(self, amount):
        """입금"""
        if not self.is_active:
            raise ValueError("비활성화된 계좌입니다")
        
        if amount <= 0:
            raise ValueError("입금액은 0보다 커야 합니다")
        
        self.__balance += amount
        Account.total_balance += amount
        
        transaction = Transaction("deposit", amount, self.__balance)
        self.__transactions.append(transaction)
        
        return True, f"{amount:,}원이 입금되었습니다. (잔액: {self.__balance:,}원)"
    
    def withdraw(self, amount):
        """출금"""
        if not self.is_active:
            raise ValueError("비활성화된 계좌입니다")
        
        if amount <= 0:
            raise ValueError("출금액은 0보다 커야 합니다")
        
        if amount > self.__balance:
            raise ValueError(f"잔액이 부족합니다. (현재 잔액: {self.__balance:,}원)")
        
        self.__balance -= amount
        Account.total_balance -= amount
        
        transaction = Transaction("withdrawal", amount, self.__balance)
        self.__transactions.append(transaction)
        
        return True, f"{amount:,}원이 출금되었습니다. (잔액: {self.__balance:,}원)"
    
    def transfer(self, target_account, amount):
        """계좌 이체"""
        if not isinstance(target_account, Account):
            raise TypeError("유효한 계좌가 아닙니다")
        
        if target_account == self:
            raise ValueError("같은 계좌로는 이체할 수 없습니다")
        
        # 출금 시도
        try:
            self.withdraw(amount)
            
            # 출금 성공시 입금
            try:
                target_account.deposit(amount)
                
                # 거래 내역 수정
                self.__transactions[-1].type = "transfer_out"
                self.__transactions[-1].description = f"→ {target_account.account_number}"
                
                target_account.__transactions[-1].type = "transfer_in"
                target_account.__transactions[-1].description = f"← {self.account_number}"
                
                return True, f"{amount:,}원을 {target_account.account_number}로 이체했습니다"
                
            except Exception as e:
                # 입금 실패시 출금 취소
                self.__balance += amount
                Account.total_balance += amount
                self.__transactions.pop()
                raise e
                
        except Exception as e:
            raise e
    
    def get_transactions(self, limit=None, transaction_type=None):
        """거래 내역 조회"""
        transactions = self.__transactions.copy()
        
        # 타입별 필터링
        if transaction_type:
            transactions = [t for t in transactions if t.type == transaction_type]
        
        # 최근 거래부터 반환
        transactions.reverse()
        
        if limit:
            return transactions[:limit]
        
        return transactions
    
    def get_account_summary(self):
        """계좌 요약 정보"""
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
        """계좌 폐쇄"""
        if self.__balance > 0:
            raise ValueError(f"잔액이 있는 계좌는 폐쇄할 수 없습니다. (잔액: {self.__balance:,}원)")
        
        self.is_active = False
        Account.total_accounts -= 1
        
        account_type = self.__class__.__name__
        Account.account_types[account_type] -= 1
        
        return True, "계좌가 폐쇄되었습니다"
    
    @classmethod
    def get_bank_statistics(cls):
        """은행 전체 통계"""
        return {
            'bank_name': cls.bank_name,
            'total_accounts': cls.total_accounts,
            'total_balance': cls.total_balance,
            'average_balance': cls.total_balance / cls.total_accounts if cls.total_accounts > 0 else 0,
            'account_types': dict(cls.account_types)
        }
    
    @classmethod
    def generate_account_number(cls):
        """계좌번호 생성"""
        timestamp = datetime.now().strftime('%Y%m%d')
        random_digits = ''.join(random.choices(string.digits, k=6))
        return f"{timestamp}-{random_digits}"
    
    @staticmethod
    def validate_account_number(account_number):
        """계좌번호 유효성 검사"""
        import re
        # YYYYMMDD-XXXXXX 형식
        pattern = r'^\d{8}-\d{6}'
        return re.match(pattern, account_number) is not None
    
    @staticmethod
    def format_currency(amount):
        """통화 형식으로 포맷팅"""
        return f"₩{amount:,.0f}"
    
    def __str__(self):
        return (f"{self.__class__.__name__} - {self.account_number}\n"
                f"예금주: {self.owner_name}\n"
                f"잔액: {self.format_currency(self.__balance)}")
    
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.account_number}', '{self.owner_name}', {self.__balance})"

class SavingsAccount(Account):
    """저축 예금 계좌"""
    
    def __init__(self, account_number, owner_name, interest_rate, initial_balance=0):
        super().__init__(account_number, owner_name, initial_balance)
        self.interest_rate = interest_rate  # 연 이율 (%)
        self.last_interest_date = datetime.now()
        self.minimum_balance = 10000  # 최소 잔액
    
    def add_monthly_interest(self):
        """월 이자 지급"""
        # 마지막 이자 지급일로부터 30일 경과 확인
        days_passed = (datetime.now() - self.last_interest_date).days
        
        if days_passed < 30:
            return False, f"이자 지급일이 아닙니다. ({30 - days_passed}일 후 지급)"
        
        # 월 이자 계산 (연이율 / 12)
        monthly_rate = self.interest_rate / 12 / 100
        interest = int(self.balance * monthly_rate)
        
        if interest > 0:
            self._Account__balance += interest  # 부모 클래스의 private 속성 접근
            Account.total_balance += interest
            
            transaction = Transaction("interest", interest, self.balance, 
                                    f"월 이자 (연 {self.interest_rate}%)")
            self._Account__transactions.append(transaction)
            
            self.last_interest_date = datetime.now()
            
            return True, f"이자 {interest:,}원이 지급되었습니다"
        
        return False, "이자가 0원입니다"
    
    def withdraw(self, amount):
        """출금 (최소 잔액 확인)"""
        if self.balance - amount < self.minimum_balance:
            raise ValueError(f"최소 잔액 {self.minimum_balance:,}원을 유지해야 합니다")
        
        return super().withdraw(amount)

class CheckingAccount(Account):
    """입출금 계좌 (마이너스 통장)"""
    
    def __init__(self, account_number, owner_name, overdraft_limit=0, initial_balance=0):
        super().__init__(account_number, owner_name, initial_balance)
        self.overdraft_limit = overdraft_limit  # 마이너스 한도
        self.overdraft_fee_rate = 0.1  # 마이너스 수수료율 (일 0.1%)
        self.last_fee_date = datetime.now()
    
    def withdraw(self, amount):
        """출금 (마이너스 한도까지 가능)"""
        if not self.is_active:
            raise ValueError("비활성화된 계좌입니다")
        
        if amount <= 0:
            raise ValueError("출금액은 0보다 커야 합니다")
        
        # 출금 후 잔액이 마이너스 한도를 초과하는지 확인
        if self.balance - amount < -self.overdraft_limit:
            available = self.balance + self.overdraft_limit
            raise ValueError(f"한도를 초과합니다. (출금 가능액: {available:,}원)")
        
        # 부모 클래스의 private 속성 직접 수정
        self._Account__balance -= amount
        Account.total_balance -= amount
        
        transaction = Transaction("withdrawal", amount, self.balance)
        self._Account__transactions.append(transaction)
        
        # 마이너스 잔액 경고
        if self.balance < 0:
            return True, f"{amount:,}원 출금. 마이너스 잔액: {self.balance:,}원"
        
        return True, f"{amount:,}원이 출금되었습니다. (잔액: {self.balance:,}원)"
    
    def charge_overdraft_fee(self):
        """마이너스 이자 부과"""
        if self.balance >= 0:
            return False, "마이너스 잔액이 없습니다"
        
        days_passed = (datetime.now() - self.last_fee_date).days
        if days_passed < 1:
            return False, "이미 오늘 수수료가 부과되었습니다"
        
        # 일일 수수료 계산
        daily_fee = int(abs(self.balance) * self.overdraft_fee_rate / 100)
        
        if daily_fee > 0:
            self._Account__balance -= daily_fee
            Account.total_balance -= daily_fee
            
            transaction = Transaction("fee", daily_fee, self.balance,
                                    f"마이너스 이자 ({days_passed}일)")
            self._Account__transactions.append(transaction)
            
            self.last_fee_date = datetime.now()
            
            return True, f"마이너스 이자 {daily_fee:,}원이 부과되었습니다"
        
        return False, "수수료가 0원입니다"

class FixedDepositAccount(Account):
    """정기 예금 계좌"""
    
    def __init__(self, account_number, owner_name, interest_rate, term_months, initial_balance=0):
        super().__init__(account_number, owner_name, initial_balance)
        self.interest_rate = interest_rate  # 연 이율
        self.term_months = term_months  # 예치 기간 (개월)
        self.maturity_date = self._calculate_maturity_date()
        self.is_matured = False
        self.early_withdrawal_penalty = 0.5  # 중도 해지 수수료 50%
    
    def _calculate_maturity_date(self):
        """만기일 계산"""
        from dateutil.relativedelta import relativedelta
        return self.created_at + relativedelta(months=self.term_months)
    
    def deposit(self, amount):
        """추가 입금 불가"""
        if len(self._Account__transactions) > 1:
            raise ValueError("정기예금은 추가 입금이 불가능합니다")
        return super().deposit(amount)
    
    def withdraw(self, amount):
        """출금 (만기 또는 중도해지)"""
        if datetime.now() >= self.maturity_date:
            # 만기 출금
            if not self.is_matured:
                self._add_maturity_interest()
                self.is_matured = True
            
            return super().withdraw(amount)
        else:
            # 중도 해지
            return self._early_withdrawal(amount)
    
    def _add_maturity_interest(self):
        """만기 이자 지급"""
        # 단리 이자 계산
        total_interest = int(self.balance * self.interest_rate / 100 * self.term_months / 12)
        
        self._Account__balance += total_interest
        Account.total_balance += total_interest
        
        transaction = Transaction("interest", total_interest, self.balance,
                                f"만기 이자 ({self.term_months}개월, 연 {self.interest_rate}%)")
        self._Account__transactions.append(transaction)
    
    def _early_withdrawal(self, amount):
        """중도 해지"""
        # 경과 기간 계산
        months_passed = (datetime.now() - self.created_at).days // 30
        
        # 일부 이자 계산 (패널티 적용)
        partial_interest = int(
            self.balance * self.interest_rate / 100 * months_passed / 12 
            * (1 - self.early_withdrawal_penalty)
        )
        
        self._Account__balance += partial_interest
        Account.total_balance += partial_interest
        
        transaction = Transaction("interest", partial_interest, self.balance,
                                f"중도해지 이자 ({months_passed}개월, 패널티 {self.early_withdrawal_penalty*100}%)")
        self._Account__transactions.append(transaction)
        
        # 전액 출금
        if amount == self.balance:
            return super().withdraw(amount)
        else:
            raise ValueError("정기예금은 중도해지시 전액 출금만 가능합니다")
    
    def get_maturity_info(self):
        """만기 정보 조회"""
        days_remaining = (self.maturity_date - datetime.now()).days
        expected_interest = int(self.balance * self.interest_rate / 100 * self.term_months / 12)
        
        return {
            'maturity_date': self.maturity_date.strftime('%Y-%m-%d'),
            'days_remaining': max(0, days_remaining),
            'expected_interest': expected_interest,
            'expected_total': self.balance + expected_interest,
            'is_matured': days_remaining <= 0
        }

def demo_bank_system():
    """은행 시스템 데모"""
    print("=== 파이썬 은행 시스템 데모 ===\n")
    
    # 1. 다양한 계좌 생성
    print("1. 계좌 생성")
    
    # 입출금 계좌
    checking = CheckingAccount(
        Account.generate_account_number(),
        "김철수",
        overdraft_limit=1000000,
        initial_balance=500000
    )
    print(f"입출금 계좌 생성: {checking.account_number}")
    
    # 저축 계좌
    savings = SavingsAccount(
        Account.generate_account_number(),
        "이영희",
        interest_rate=3.5,
        initial_balance=2000000
    )
    print(f"저축 계좌 생성: {savings.account_number}")
    
    # 정기 예금
    fixed = FixedDepositAccount(
        Account.generate_account_number(),
        "박민수",
        interest_rate=4.5,
        term_months=12,
        initial_balance=5000000
    )
    print(f"정기예금 계좌 생성: {fixed.account_number}")
    
    print("\n" + "-"*50 + "\n")
    
    # 2. 거래 실행
    print("2. 거래 실행\n")
    
    # 입금
    success, msg = checking.deposit(300000)
    print(f"입금: {msg}")
    
    # 출금
    success, msg = checking.withdraw(1000000)
    print(f"출금: {msg}")
    
    # 마이너스 출금
    success, msg = checking.withdraw(500000)
    print(f"마이너스 출금: {msg}")
    
    # 계좌 이체
    success, msg = savings.transfer(checking, 500000)
    print(f"이체: {msg}")
    
    print("\n" + "-"*50 + "\n")
    
    # 3. 이자 처리
    print("3. 이자 처리\n")
    
    # 저축 계좌 이자
    savings.last_interest_date = datetime.now() - timedelta(days=31)  # 테스트를 위해 날짜 조정
    success, msg = savings.add_monthly_interest()
    print(f"저축계좌: {msg}")
    
    # 마이너스 이자
    checking.last_fee_date = datetime.now() - timedelta(days=1)  # 테스트를 위해 날짜 조정
    success, msg = checking.charge_overdraft_fee()
    print(f"입출금계좌: {msg}")
    
    # 정기예금 만기 정보
    maturity_info = fixed.get_maturity_info()
    print(f"정기예금 만기일: {maturity_info['maturity_date']}")
    print(f"예상 만기 금액: {maturity_info['expected_total']:,}원")
    
    print("\n" + "-"*50 + "\n")
    
    # 4. 계좌 조회
    print("4. 계좌 정보 조회\n")
    
    accounts = [checking, savings, fixed]
    for account in accounts:
        print(account)
        print()
    
    # 5. 거래 내역
    print("5. 최근 거래 내역\n")
    
    print(f"{checking.owner_name}님의 거래 내역:")
    for transaction in checking.get_transactions(limit=5):
        print(f"  {transaction}")
    
    print("\n" + "-"*50 + "\n")
    
    # 6. 은행 통계
    print("6. 은행 전체 통계\n")
    
    stats = Account.get_bank_statistics()
    print(f"은행명: {stats['bank_name']}")
    print(f"총 계좌 수: {stats['total_accounts']}")
    print(f"총 예치금: {stats['total_balance']:,}원")
    print(f"평균 잔액: {stats['average_balance']:,.0f}원")
    print(f"계좌 유형별: {stats['account_types']}")

if __name__ == "__main__":
    from datetime import timedelta
    demo_bank_system()