import os
from streaming import create_m3u8
from threading import Thread


PATH = "static/shows"
shows = os.listdir(PATH)

numbers = "0123456789"


for show in shows:
    SHOW_PATH = f"{PATH}/{show}"
    seasons = os.listdir(SHOW_PATH)
    for season in seasons:
        if season.isdigit():
            SEASON_PATH = f"{SHOW_PATH}/{season}"
            episodes = [episode for episode in os.listdir(SEASON_PATH) if os.path.isfile(f"{SEASON_PATH}/{episode}")]
        else:
            continue
        for j in range(len(episodes)):
            episode = episodes[j]
            EPISODE_PATH = f"{SEASON_PATH}/{episode}"
            name, extention = episode.rsplit(".", 1)
            NEW_PATH = f"{SEASON_PATH}/{j + 1}.{extention}"
            if not episode.isdigit() and not os.path.isfile(NEW_PATH):
                os.rename(EPISODE_PATH, NEW_PATH)
            m3u8_folder = f"{SEASON_PATH}/{j + 1}"
            if not os.path.isdir(m3u8_folder):
                os.mkdir(m3u8_folder)
                create_m3u8(NEW_PATH, m3u8_folder)
