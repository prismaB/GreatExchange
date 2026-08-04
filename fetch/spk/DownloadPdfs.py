import httpx
import asyncio
from pathlib import Path as p
class DownloadFile:
    def __init__(self,spk_pdf_url: str, spk_pdf_kayit_klasoru):
        self.spk_pdf_url = spk_pdf_url
        self.__spk_pdf_kayit_klasoru = p.cwd() +"/GreatExchange"
        path = p(self.__spk_pdf_kayit_klasoru) / "bultenler" / "2026"

    async def DownloadPdf(self,path):
        if path.exists():
            async with httpx.AsyncClient(verify=False,follow_redirects=True,timeout=45) as client:
                try:
                    req = await client.get(self.spk_pdf_url)
                    try:
                        path.write_bytes(req.content)
                    except PermissionError:
                        pass #logla
                except ConnectionRefusedError as err:
                    pass #logger modülü ile loglama yapacağım
        else:
            path.mkdir(parents=True,exist_ok=True)
            await self.DownloadPdf()