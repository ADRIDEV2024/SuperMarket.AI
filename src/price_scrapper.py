import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sqlite3
import time



class PriceScrapper:

    def __init__(self, urls, db_path="markets_database.db", max_retries=3):
        self.urls = urls 
        self.db_path = db_path
        self.max_retries = max_retries
        self._init_db():
        self.urls = urls  # Lista de URLs de productos o categorías


    def _init_db(self):
        """Crea la tabla si no existe."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                price TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    async def fetch(self, session, url, retries=1):
        try:
            async with session.get(url, timeout=15) as response:
                return await response.text()
        except Exception as e:
            if retries < self.max_retries:
                await asyncio.sleep(2 ** retries)  # Exponential backoff
                return await self.fetch(session, url, retries + 1)
            print(f"Error al obtener {url}: {e}")
            return None

    async def scrape_price(self, url):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, url)
            soup = BeautifulSoup(html, "html.parser")
            # Ajusta el selector según la tienda
            price_tag = soup.select_one(".price, .product-price, [data-price]")
            if price_tag:
                price = price_tag.get_text(strip=True)
                return {"url": url, "price": price}
            return {"url": url, "price": None}

    async def scrape_all(self):
        tasks = [self.scrape_price(url) for url in self.urls]
        return await asyncio.gather(*tasks)
    

    
    def save_to_db(self, url, price):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prices (url, price) VALUES (?, ?)",
            (url, price)
        )
        conn.commit()
        conn.close()

if __name__ == "__main__":

    urls = ["https://dia.es/search?q=productos", "https://info.mercadona.es/es/supermercados/search?q=productos"]
    scrapper = PriceScrapper(urls)
    results = asyncio.run(scrapper.scrape_all())
    print(results)