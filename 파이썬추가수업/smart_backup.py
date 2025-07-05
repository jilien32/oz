import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import zipfile

class SmartBackup:
    def __init__(self, source_dir, backup_dir):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        self.history_file = self.backup_dir / 'backup_history.json'
        self.load_history()

    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = {}
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def need_backup(self, file_path):
        str_path = str(file_path)
        if str_path not in self.history:
            return True
        
        last_modified = file_path.stat().st_mtime
        return last_modified > self.history[str_path]
    
    def backup(self, compress=False):
        backup_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        if compress:
            backup_path = self.backup_dir / f'backup_{backup_time}.zip'
            with zipfile.ZipFile(backup_path, 'w') as zf:
                for file_path in self.source_dir.rglob('*'):
                    if file_path.is_file() and self.need_backup(file_path):
                        arcname = file_path.relative_to(self.source_dir)
                        zf.write(file_path, arcname)
                        self.history[str(file_path)] = file_path.stat().st_mtime
                        print(f"백업: {arcname}")

        else:
            backup_path = self.backup_dir / f'backup_{backup_time}'
            backup_path.mkdir()

            for file_path in self.source_dir.rglob('*'):
                if file_path.is_file() and self.need_backup(file_path):
                    relative_path = file_path. relative_to(self.source_dir)
                    dest_path = backup_path / relative_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    self.history[str(file_path)] = file_path.stat().st_mtime
                    print(f"백업: {relative_path}")
        self.save_history()
        print(f"\n백업 완료: {backup_path}")

backup = SmartBackup('my_project', 'backups')
backup.backup(compress=True)
backup.backup()