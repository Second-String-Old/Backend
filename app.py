import os
import nflgame
import json
import datetime
import itertools

from flask import Flask
from flask_cors import CORS
from flask import request
app = Flask(__name__, instance_relative_config=True)
CORS(app)

def create_app(test_config=None):
    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app    

def makeResponse(payload):
    data = {}
    data['Data'] = payload
    return json.dumps(data)

# Function for adding stats to a dictionary to keep code nice and clean
# This will have dual use as it will make adding the individual routes way easier/cleaner
def addStats(dict, stats, pos):
    if pos == 'QB':
        dict['player_name'] = stats.player.full_name
        dict['player_team'] = stats.team
        dict['passing_cmp'] = stats.passing_cmp
        dict['passing_att'] = stats.passing_att
        dict['passing_tds'] = stats.passing_tds
        dict['passing_yds'] = stats.passing_yds
        dict['passing_int'] = stats.passing_int
        dict['passing_sk'] = stats.passing_sk
        dict['rushing_att'] = stats.rushing_att
        dict['rushing_yds'] = stats.rushing_yds
    elif pos == 'WR':
        dict['player_name'] = stats.player.full_name
        dict['player_team'] = stats.team
        dict['receiving_rec'] = stats.receiving_rec
        dict['receiving_tar'] = stats.receiving_tar
        dict['receiving_tds'] = stats.receiving_tds
        dict['receiving_yds'] = stats.receiving_yds
        dict['rushing_att'] = stats.rushing_att
        dict['rushing_yds'] = stats.rushing_yds
        dict['rushing_tds'] = stats.rushing_tds
    elif pos == 'RB':
        dict['player_name'] = stats.player.full_name
        dict['player_team'] = stats.team
        dict['receiving_rec'] = stats.receiving_rec
        dict['receiving_tar'] = stats.receiving_tar
        dict['receiving_tds'] = stats.receiving_tds
        dict['receiving_yds'] = stats.receiving_yds
        dict['rushing_att'] = stats.rushing_att
        dict['rushing_yds'] = stats.rushing_yds
        dict['rushing_loss_yds'] = stats.rushing_loss_yds
        dict['rushing_tds'] = stats.rushing_tds
    return dict

# a simple response that returns top 5 rushing yards
@app.route('/players/test/')
def test():
    games = nflgame.games(2018, week=5)
    players = nflgame.combine_game_stats(games)
    testPL = []
    for p in players.rushing().sort('rushing_yds').limit(25):
        msg = '%s %d carries for %d yards and %d TDs'
        testPL.append(msg % (p, p.rushing_att, p.rushing_yds, p.rushing_tds))
    return makeResponse(testPL)

passing_attrs = ['passing_cmp', 'passing_att', 'passing_tds', 'passing_yds', 'passing_int', 'passing_sk']

# /players/QB/?count={count}&year={year}&week={week}
@app.route('/players/QB/')
def qb():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 10
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    games = nflgame.games(int(year), week=1)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.passing().sort('passing_yds').limit(int(count)):
        player = addStats({'pos':'QB'}, p, 'QB')
        playerList.append(player)
    return makeResponse(playerList)

# Deprecated ?
# /players/rec/?count={count}&year={year}&week={week}
@app.route('/players/rec/')
def rec():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 10
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    print(count, year, week)
    games = nflgame.games(int(year), week=week)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.receiving().sort('receiving_yds').limit(int(count)):
        # print(p.guess_position)
        player = addStats({}, p, 'WR')
        playerList.append(player)
    return makeResponse(playerList)

# /players/WR/?count={count}&year={year}&week={week}
@app.route('/players/WR/')
def WR():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 10
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    print(count, year, week)
    games = nflgame.games(int(year), week=week)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.receiving().sort('receiving_yds').limit(int(count)):
        if p.guess_position == 'WR':
            player = addStats({'pos':'WR'}, p, 'WR')
            playerList.append(player)
    return makeResponse(playerList)

# /players/TE/?count={count}&year={year}&week={week}
@app.route('/players/TE/')
def TE():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 10
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    print(count, year, week)
    games = nflgame.games(int(year), week=week)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.receiving().sort('receiving_yds').limit(int(count)):
        # print(p.guess_position)
        if p.guess_position == 'TE':
            player = addStats({'pos':'TE'}, p, 'WR')
            playerList.append(player)
    return makeResponse(playerList)

# /players/RB/?count={count}&year={year}&week={week}
@app.route('/players/RB/')
def rb():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 10
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    print(count, year, week)
    games = nflgame.games(int(year), week=week)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.rushing().sort('rushing_yds').limit(int(count)):
        player = addStats({'pos':'RB'}, p, 'RB')
        playerList.append(player)
    return makeResponse(playerList)

# /players/?&name={name}&team{team}&year={year}&week={week}
@app.route('/players/')
def player():
    year = request.args.get('year')
    week = request.args.get('week')
    name = request.args.get('name')
    team = request.args.get('team')
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    name = 'Drew Brees'
    team = 'NO'
    games = nflgame.games(int(year), week=week)
    players = nflgame.combine_game_stats(games)
    player = nflgame.find(name, team=team)[0]

    for x in players:
        if x.name == player.gsis_name:
            p = addStats(player.__dict__, x, player.position)
    return makeResponse([p])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=port)  