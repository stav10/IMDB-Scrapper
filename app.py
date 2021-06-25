from flask import Flask, jsonify, request
import json
from DB import LocalDb

app = Flask(__name__)

db = LocalDb('static/series.json')


@app.route("/")
def index():
    return "hello world"


@app.route('/shows')
def get_shows_data():
    with open('static/series.json', 'r') as f:
        data = json.load(f)
        print(jsonify(data))
        return jsonify(data)


@app.route("/shows/<string:name>/<string:season>")
def season_page_data(name, season):
    return jsonify(get_season_data(name, season))


@app.route("/shows/<string:name>/<string:season>/<string:episodeNum>")
def episode_page_data(name, season, episodeNum):
    season_data = get_season_data(name, season)['episodes']

    episode_data = list(filter(lambda x: x['episodeNum'] == int(episodeNum), season_data))[0]
    return episode_data if episode_data else None


def get_season_data(name, season):
    show = db.find_one({"name": name})
    if show and len(show['seasons']) >= int(season):
        data = list(filter(lambda x: list(x.keys())[0] == season, show['seasons']))[0][season]
        return {"episodes": data, "showImg": show['imageUrl'], 'seasonNum': len(show['seasons'])}
    return None


@app.after_request
def after(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return res


app.run(host="127.0.0.1", port=8000)
