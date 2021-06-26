from flask import Flask, jsonify, request
import json
from DB import LocalDb
from scrapper_utils import scrap_suggestion

app = Flask(__name__)

db = LocalDb('static/series.json')


@app.route("/")
def index():
    return "hello world"


@app.route('/shows')
def get_shows_data():
    shows_data = [{"id": show['id'], "name": show['name'], "imageUrl": show.get('imageUrl')} for show in db.find_all()]
    return jsonify(shows_data)

@app.route("/shows/names")
def get_shows_name():
    shows_data = db.find_all()
    shows_names = [show['name'] for show in shows_data]
    return jsonify(shows_names)


@app.route("/shows/<string:name>/<string:season>")
def season_page_data(name, season):
    return jsonify(get_season_data(name, season))


@app.route("/shows/<string:name>/<string:season>/<string:episodeNum>")
def episode_page_data(name, season, episodeNum):
    season_data = get_season_data(name, season)['episodes']

    episode_data = list(filter(lambda x: x['episodeNum'] == int(episodeNum), season_data))[0]
    return episode_data if episode_data else None


@app.route("/showsSuggestion/<string:search_text>")
def get_suggestions(search_text):
    sugs = scrap_suggestion(search_text)
    return jsonify(sugs)


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


app.run(host="0.0.0.0", port=8000)
