import requests
from bs4 import BeautifulSoup

id = "series_popup"

show_name = input("please enter a show")

url = f"https://medovavim.com/main/search?search_movie={show_name}"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

html = requests.get(url, headers)

soup = BeautifulSoup(html.content, 'html.parser')
