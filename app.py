import os
import nflgame
import json

from flask import Flask
from flask import request
app = Flask(__name__, instance_relative_config=True)

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
        count = 25
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    games = nflgame.games(int(year), week=week)
    print(games)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.passing().sort('passing_yds').limit(int(count)):
        player = {}
        player['player_name'] = p.name
        player['player_team'] = p.team
        player['passing_cmp'] = p.passing_cmp
        player['passing_att'] = p.passing_att
        player['passing_tds'] = p.passing_tds
        player['passing_yds'] = p.passing_yds
        player['passing_int'] = p.passing_int
        player['passing_sk'] = p.passing_sk
        player['russing_att'] = p.rushing_att
        player['rushing_yds'] = p.rushing_yds
        playerList.append(player)
    return makeResponse(playerList)

# /players/WR/?count={count}&year={year}&week={week}
@app.route('/players/WR/')
def wr():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 25
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    print(count, year, week)
    games = nflgame.games(int(year), week=week)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.receiving().sort('receiving_yds').limit(int(count)):
        print(p.guess_position)
        player = {}
        player['player_name'] = p.name
        player['player_team'] = p.team
        player['receiving_rec'] = p.receiving_rec
        player['receiving_tar'] = p.receiving_tar
        player['receiving_tds'] = p.receiving_tds
        player['receiving_yds'] = p.receiving_yds
        player['russing_att'] = p.rushing_att
        player['rushing_yds'] = p.rushing_yds
        playerList.append(player)
    return makeResponse(playerList)

# /players/RB/?count={count}&year={year}&week={week}
@app.route('/players/RB/')
def rb():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 25
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    print(count, year, week)
    games = nflgame.games(int(year), week=week)
    players = nflgame.combine_game_stats(games)
    playerList = []
    for p in players.rushing().sort('rushing_yds').limit(int(count)):
        player = {}
        player['player_name'] = p.name
        player['player_team'] = p.team
        player['receiving_rec'] = p.receiving_rec
        player['receiving_tar'] = p.receiving_tar
        player['receiving_tds'] = p.receiving_tds
        player['receiving_yds'] = p.receiving_yds
        player['russing_att'] = p.rushing_att
        player['rushing_yds'] = p.rushing_yds
        player['rushing_loss_yds'] = p.rushing_loss_yds
        player['rushing_tds'] = p.rushing_tds
        playerList.append(player)
    return makeResponse(playerList)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=port)