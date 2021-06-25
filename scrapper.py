import requests
from bs4 import BeautifulSoup
from DB import LocalDb

db = LocalDb('series.json')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

show = input("enter a show search: ")

url = f"https://v2.sg.media-imdb.com/suggestion/{show[0]}/{show}.json"

data = requests.get(url, headers=headers).json()['d']


show_series_data = []


def show_matches(show, index):
    print(f"{index + 1}: {show['l']}")
    return {"name": show['l'], "id": show['id'], 'imageUrl': show['i']['imageUrl']}


def parse_html(html_soup):
    season_episodes = html_soup.find_all("div", class_="list_item")
    episodes = []
    for episode in season_episodes:
        title = episode.find("strong").find("a")['title']
        description = episode.find("div", class_="item_description").text
        image_url = episode.find("img", class_="zero-z-index")
        image_url = image_url['src'] if image_url else None
        rating = episode.find("span", class_="ipl-rating-star__rating").text
        episodeNum = int(episode.find("meta", {"itemprop": "episodeNumber"})['content'])
        episodes.append({"title": title, "episodeNum": episodeNum, "description": description, "imageUrl": image_url, "rating": rating, "id": episodeNum})
    return episodes


print()

potential_matches = [show_matches(data[i], i) for i in range(len(data))]

show_index = int(input("\nplease enter your show number: ")) - 1
show = potential_matches[show_index]

print(show)
show_url = f"https://www.imdb.com/title/{show['id']}/episodes/_ajax?season=1"
req = requests.get(show_url, headers=headers)
soup = BeautifulSoup(req.content, 'html.parser')
num_of_seasons = int(soup.find("select", id="bySeason").find_all("option")[-1]['value'])

for i in range(num_of_seasons):
    show_url = f"https://www.imdb.com/title/{show['id']}/episodes/_ajax?season={i + 1}"
    req = requests.get(show_url, headers=headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        show_series_data.append({f"{i + 1}": parse_html(soup)})
    else:
        break

db.insert_one({'name': show['name'], 'imageUrl': show['imageUrl'], 'seasons': show_series_data})
