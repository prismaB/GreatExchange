import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

class Logger:
    def __init__(self, config_path: Optional[Path] = None):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.config_path = config_path or (self.base_dir / "config.json")
        
        self.paths: Dict[str, Path] = {}
        self._load_config()
        self._init_databases()

    def _load_config(self) -> None:
        if not self.config_path.exists():
            alt_path = Path.cwd() / "config.json"
            if alt_path.exists():
                self.config_path = alt_path
            else:
                raise FileNotFoundError(f"Config dosyası bulunamadı: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        dir_config = config_data.get("Directory", {})
        self.log_dir = self.base_dir / dir_config.get("directory", "GreatExchange/logs/")
        self.paths = {
            "error": self.base_dir / dir_config.get("errorlog", "GreatExchange/logs/error.db"),
            "install": self.base_dir / dir_config.get("installHistorylog", "GreatExchange/logs/Ihistory.db"),
            "fetch": self.base_dir / dir_config.get("fetchLog", "GreatExchange/logs/fetch.db")
        }
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _init_databases(self) -> None:
        with sqlite3.connect(self.paths["error"]) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS error_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT NOT NULL,
                    error TEXT NOT NULL
                )
            """)

        with sqlite3.connect(self.paths["fetch"]) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fetch_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT NOT NULL,
                    message TEXT NOT NULL
                )
            """)

        with sqlite3.connect(self.paths["install"]) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS install_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT NOT NULL,
                    action TEXT NOT NULL
                )
            """)

    def log_error(self, error_message: str) -> None:
        now = datetime.now().isoformat()
        with sqlite3.connect(self.paths["error"]) as conn:
            conn.execute("INSERT INTO error_logs (datetime, error) VALUES (?, ?)", (now, str(error_message)))

    def log_fetch(self, message: str) -> None:
        """Fetch işlemlerini fetch.db tablosuna yazar."""
        now = datetime.now().isoformat()
        with sqlite3.connect(self.paths["fetch"]) as conn:
            conn.execute("INSERT INTO fetch_logs (datetime, message) VALUES (?, ?)", (now, str(message)))

    def log_install(self, action: str) -> None:
        now = datetime.now().isoformat()
        with sqlite3.connect(self.paths["install"]) as conn:
            conn.execute("INSERT INTO install_logs (datetime, action) VALUES (?, ?)", (now, str(action)))

logger = Logger()
if __name__ == "__main__":
    test_logger = Logger()
    test_logger.log_fetch("Logger başarıyla başlatıldı.")
    test_logger.log_error("Örnek hata kaydı.")
    print("Log yolları:", test_logger.paths)