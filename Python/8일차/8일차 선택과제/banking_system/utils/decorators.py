from typing import Callable

def validate_transaction(func: Callable) -> Callable:
    def wrapper(amount: int, *args, **kwargs):
        # 거래 금액 검증
        if amount <= 0:
            raise ValueError("거래 금액은 0보다 커야 합니다.")

        # 원래 함수 실행
        return func(amount, *args, **kwargs)
    
    return wrapper
