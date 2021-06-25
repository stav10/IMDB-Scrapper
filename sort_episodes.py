import os


PATH = "static/shows"
shows = os.listdir(PATH)

numbers = "0123456789"

for show in shows:
    SHOW_PATH = f"{PATH}/{show}"
    seasons = os.listdir(SHOW_PATH)
    for season in seasons:
        if season.isdigit():
            SEASON_PATH = f"{SHOW_PATH}/{season}"
            episodes = os.listdir(SEASON_PATH)
        else:
            continue
        for j in range(len(episodes)):
            episode = episodes[j]
            if not episode.isdigit():
                EPISODE_PATH = f"{SEASON_PATH}/{episode}"
                name, extention = episode.rsplit(".", 1)
                os.rename(EPISODE_PATH, f"{SEASON_PATH}/{j+1}.{extention}")


