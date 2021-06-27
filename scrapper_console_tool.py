import requests
from bs4 import BeautifulSoup
from DB import LocalDb
import os
from re import search

db = LocalDb('static/series.json')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

show = input("enter a show search: ")

url = f"https://v2.sg.media-imdb.com/suggestion/{show[0]}/{show}.json"

data = requests.get(url, headers=headers).json()['d']

show_series_data = []


def show_matches(show, index):
    print(f"{index + 1}: {show['l']}")
    return {"name": show['l'], "id": show['id'], 'imageUrl': show['i']['imageUrl'] if show.get('i') else None}


def get_show_name(imdb_show_name):
    PATH = "static/shows"
    shows = os.listdir(PATH)
    for path_show in shows:
        if search(path_show.lower(), imdb_show_name.lower()) or search(imdb_show_name.lower(), path_show.lower()):
            return path_show
    return imdb_show_name


def create_url(path, episodeNum):
    if os.path.exists(path) and os.path.isfile(path):
        files = os.listdir(path)
        for f in files:
            file_name, extension = f.split(".")
            if int(file_name) == int(episodeNum):
                return f"{path}/{file_name}/hls.m3u8"
    return f"{path}/{episodeNum}/hls.m3u8"


def parse_html(html_soup, season):
    season_episodes = html_soup.find_all("div", class_="list_item")
    episodes = []
    for episode in season_episodes:
        title = episode.find("strong").find("a")['title']
        description = episode.find("div", class_="item_description").text
        image_url = episode.find("img", class_="zero-z-index")
        image_url = image_url['src'] if image_url else None
        rating = episode.find("span", class_="ipl-rating-star__rating")
        rating = rating.text if rating else None
        episodeNum = int(episode.find("meta", {"itemprop": "episodeNumber"})['content'])
        episodes.append({"title": title, "episodeNum": episodeNum, "description": description, "imageUrl": image_url,
                         "videoUrl": create_url(f"static/shows/{get_show_name(show['name'])}/{season}", episodeNum),
                         "rating": rating, "id": episodeNum})
    return episodes


print()

potential_matches = [show_matches(data[i], i) for i in range(len(data))]

show_index = int(input("\nplease enter your show number: ")) - 1
show = potential_matches[show_index]

print(show)
show_url = f"https://www.imdb.com/title/{show['id']}/episodes/_ajax?season=1"
req = requests.get(show_url, headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')
html_seasons = soup.find("select", id="bySeason").find_all("option")
num_of_seasons = int(html_seasons[-2]['value']) if int(html_seasons[-1]['value']) == -1 else int(html_seasons[-1]['value'])

print(num_of_seasons)

for i in range(num_of_seasons):
    show_url = f"https://www.imdb.com/title/{show['id']}/episodes/_ajax?season={i + 1}"
    req = requests.get(show_url, headers=headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        show_series_data.append({f"{i + 1}": parse_html(soup, i + 1)})
    else:
        break

db_search_show = db.find_one({"imdbId": show['id']})
show_new_details = {'id': db.items_count() + 1, 'name': show['name'], 'imageUrl': show['imageUrl'],
                    'imdbId': show['id'], 'seasons': show_series_data}
if db_search_show:
    print(show['id'])
    db.update_one({"imdbId": show['id']}, {"$set": show_new_details})
else:
    db.insert_one(show_new_details)