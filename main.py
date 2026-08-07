from fetch.spk.spkFetch import Spk
from fetch.spk.DownloadPdfs import DownloadFile
import asyncio 
async def spk():
    spk_client = Spk()
    bulten = await spk_client.BulteniAl(bulten_url="https://spk.gov.tr/spk-bultenleri/2026-yili-spk-bultenleri")
    for url in bulten:
        try:
            tasks = [DownloadFile(url["pdf_url"]).DownloadPdf() for url in bulten]
            await asyncio.gather(*tasks)
        except Exception as ex:
            print(ex)
    return "Done"
if __name__ =="__main__":
    try:
        run = asyncio.run(spk())
        if run == "Done":
            print("is it done")
    except KeyboardInterrupt:
        print("Bye!")