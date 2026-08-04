import asyncio
from pathlib import Path as p
import httpx
class DownloadFile:
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
                try:
                    self.file.write_bytes(req.content)
                    print(f"✅ İndirildi: {self.file.name}")
                except PermissionError:
                    pass  # logla
            except ConnectionRefusedError as err:
                pass  # logger modülü ile loglama yapacağım