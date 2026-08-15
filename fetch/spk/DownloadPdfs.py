import asyncio
import hashlib
from pathlib import Path as p
import httpx
from logger.logger import logger
class DownloadFile:
    log = logger()
    def __init__(self, spk_pdf_url):
        self.spk_pdf_url = spk_pdf_url
        self.__spk_pdf_kayit_klasoru = p.cwd()
        self.path = (p(self.__spk_pdf_kayit_klasoru) / "GreatExchange" / "bultenler" / "2026")
    async def DownloadPdf(self):
        # 1. Dosya adını ayarla
        file_name = self.spk_pdf_url.split("/")[-1]
        if not file_name.endswith(".pdf"):
            file_name += ".pdf"
        self.file = self.path / file_name
        self.path.mkdir(parents=True, exist_ok=True)
        async with httpx.AsyncClient(
            verify=False, follow_redirects=True, timeout=45
        ) as client:
            try:
                req = await client.get(self.spk_pdf_url)
                req.raise_for_status()
                excepted_size = req.headers.get("Content-Length")
                if excepted_size and int(excepted_size) != len(req.content):
                    print(f"eksik indirme {self.file.name}")
                    return False
                try:
                    if self.file.exists() and self.file.stat().st_size > 0:
                        return 
                    self.file.write_bytes(req.content)
                    memory_hash = hashlib.sha256(req.content).hexdigest()
                    disk_hash = hashlib.sha256(self.file.read_bytes()).hexdigest()
                    if memory_hash != disk_hash:
                       print(f"❌ Hash hatası (Dosya bozuk): {self.file.name}")
                       return False 
                    return f"done => {self.file.name}"
                except PermissionError:
                    pass  # logla
            except ConnectionRefusedError as err:
                pass