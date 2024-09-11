import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import sys


urls = []
result = []

def set_urls(days_back):

    for day in range(days_back):
        delta =  timedelta(days = day)
        day = datetime.now().date() - delta
        urls.append(f"https://api.nbp.pl/api/exchangerates/tables/a/{day}?format=json")

def get_date_from_url(url):
    return url[46:56]

def preview_fetch(url):

    r = requests.get(url)
    if r.status_code == 200:
        euro_price = r.json()[0]["rates"][7]["mid"]
        usd_price = r.json()[0]["rates"][1]["mid"]
    else:
        euro_price = "Brak danych"
        usd_price = "Brak danych"
    return {get_date_from_url(url): {"EUR": euro_price, "USD": usd_price}}



async def preview_fetch_async():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(days_back) as pool:
        futures = [loop.run_in_executor(pool, preview_fetch, url) for url in urls]
        result = await asyncio.gather(*futures, return_exceptions=True)
        return result

if __name__ == '__main__':

    try:
        days_back = int(sys.argv[1])
        if days_back > 10:
            days_back = 10
            print("Możesz wyświetlić ceny maksymalnie z ostatnich 10 dni.")
        elif days_back < 1:
            days_back = 1
    except:
        days_back = 3
    set_urls(days_back)

    result = asyncio.run(preview_fetch_async())
    print(result)
