from flask import Flask, render_template, request
import requests
import json
from datetime import datetime, timedelta


app = Flask(__name__)

API_KEY = "886fb776ed219d58c6e628c28cdf0983ecc43fd415671011ee1b924013302dae"

@app.route("/")
def index():
    return render_template("index.html", title="Hello")
@app.route("/rankings")
def rankings():
    tour = request.args.get("tour", "WTA")  # "ATP" or "WTA"
    start = int(request.args.get("start", 1))
    end = int(request.args.get("end", 10))

    url = f'https://api.api-tennis.com/tennis/?method=get_standings&event_type={tour}&APIkey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    players = data.get("result", [])[start-1:end]
    return render_template("rankings.html", title=f"Rankings", players=players, tour=tour, start=start, end=end)
@app.route("/matches")
def matches():
    today = datetime.now()
    enddate = today.strftime("%Y-%m-%d")
    start = today-timedelta(days = 1)
    startdate = start.strftime("%Y-%m-%d")

    url = f'https://api.api-tennis.com/tennis/?method=get_fixtures&APIkey={API_KEY}&date_start={enddate}&date_stop={enddate}'
    response = requests.get(url)
    data = response.json()
    matches = data.get("result", [])
    stop = 0
    for i in range(len(matches)):
        if matches[i]['event_status']=='Finished':
            stop = i
            break       
    return render_template("matches.html", title=f"Today's Matches", upcoming=matches[0:stop], completed=matches[stop:])
@app.route("/profiles")
def profiles():
    player = request.args.get("player")
    url = f'https://api.api-tennis.com/tennis/?method=get_players&player_key={player}&APIkey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    profiles = data.get("result", [])
    return render_template("profiles.html", title=f"Profiles", profiles = profiles)