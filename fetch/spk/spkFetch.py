import urllib
import httpx
import asyncio
import colorama
from bs4 import BeautifulSoup
import datetime
class Spk:
    def __init__(self,hisse=None):
        self.hisse = hisse
    async def BulteniAl(self,bulten_url):
        self.bulten_url = bulten_url
        Bultenler = []
        async with httpx.AsyncClient(verify=False,follow_redirects=True) as req:
            try:
                r = await req.get(url=self.bulten_url)
                if r.status_code ==200:
                    Bultenler = []
                    soup = BeautifulSoup(r.text,'html.parser')
                    liste_div = soup.find("div", class_="liste")
                    if liste_div:
                        for a_tag in liste_div.find_all("a", class_="link", href=True):
                            raw_pdf_url = a_tag["href"]
                            pdf_url = urllib.parse.urljoin(self.bulten_url, raw_pdf_url)    
                            baslik_div = a_tag.find("div", class_="liste-baslik")
                            icerik_div = a_tag.find("div", class_="liste-icerik")
                            
                            bulten_no = baslik_div.get_text(strip=True) if baslik_div else None
                            yayim_tarihi = icerik_div.get_text(strip=True) if icerik_div else None
                            
                            Bultenler.append({
                                "pdf_url": pdf_url,
                                "bulten_no": bulten_no,
                                "yayim_tarihi": yayim_tarihi
                            })
            except Exception as ex:
                print("BulteniAl hata:", ex)
        return Bultenler