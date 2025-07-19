import json
import csv
import re
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s = %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class Contact:
    def __init__(self, name, phone, email, address=''):
        self.name = name
        self.phone = self.validate_phone(phone)
        self.email = self.validate_email(email)
        self.address = address

    @staticmethod
    def validate_phone(phone):
        pattern = r'^01[0-9]-?\d{3,4}-?\d{4}$'
        if not re.match(pattern, phone):
            raise ValueError(f"잘못된 전화번호입니다: {phone}")
        return phone.replace('-', '')
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]|\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError(f"잘못된 이메일 형식입니다.: {email}")
        return email
    
    def to_dict(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }
    
class AddressBook:
    def __init__(self, filename='contacts'):
        self.filename = filename
        self.contacts = []
        self.load()
    
    def add_contact(self, contact):
        for c in self.contacts:
            if c.phone == contact.phone:
                raise ValueError(f"이미 등록한 전화번호입니다: {contact.phone}")
        self. contacts.append(contact)
        logger.info(f"연락처가 추가되었습니다: {contact.name}")
        self.save()

    def search(self, keyword):
        results = []
        for contact in self.contacts:
            if (keyword.lower() in contact.name.lower() or
                keyword in contact.phone or
                keyword.lower() in contact.email.lower()):
                results.append(contact)
        return results
    
    def save(self):
        self.backup()

        try:
            with open(f'{self.filename}.json', 'w', encoding='utf-8') as f:
                      data = [c.to_dict() for c in self.contacts]
                      json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"저장을 완료했습니다: {len(self.contacts)}개의 연락처")
        except Exception as e:
            logger.error(f"저장에 실패했습니다: {e}", exc_info=True)
            raise

    def load(self):
        json_file = Path(f'{self.filename}.json')
        csv_file = Path(f'{self.filename}.csv')

        try:
            if json_file.exists():
                with open(json_file, 'r', encoding = 'utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        contact = Contact(**item)
                        self.contacts.append(contact)
                logger.info(f"JSON에서 {len(self.contacts)}게 연락처를 로드했습니다.")
            elif csv_file.exists():
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                for row in reader:
                    contact = Contact(**row)
                    self.contacts.append(contact)
                    logger.info(f"CSV에서 {len(self.contacts)}개 연락처를 로드했습니다.")
        except Exception as e:
            logger.error(f"파일 로드에 실패했습니다: {e}", exc_info=True)
            self.contacts = []

    def backup(self):
        backup_dir = Path('backups')
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f'{self.filename}_{timestamp}.json'

        try:
            with open(backup_file, 'w', encoding='tuf-8') as f:
                data = [c.to_dict() for c in self.contacts]
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"백업 생성이 완료되었습니다: {backup_file}")
        except Exception as e:
            logger.error(f"백업 생성에 실패했습니다: {e}", exc_info=True)

    def export_csv(self, filename):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                filednames = ['name', 'phone', 'email', 'address']
                writer = csv.DictWriter(f, filednames=filednames)
                for contact in self.contacts:
                    writer.writerow(contact.to_dict())
            logger.info(f"CSV로 내보내기가 완료되었습니다: {filename}")
        except Exception as e:
            logger.error(f"CSV로 내보내기가 실패했습니다: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    book = AddressBook()

    try:
        contact = Contact('홍길동', '010-1234-5678', 'gildong@naver.com')
        book.add_contact(contact)

        results = book.search('홍')
        for c in results:
            print(f"{c.name}: {c.phone}")
    except ValueError as e:
        print(f"입력 오류: {e}")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        logger.critical("프로그램 오류", exc_info=True)