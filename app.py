import os
import nflgame
import json
import itertools
import datetime

from flask import Response
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

def fillBlanks(dict):
    for x in dict:
        if x is None:
            dict[x] = 0
    return dict

# Function for adding stats to a dictionary to keep code nice and clean
# This will have dual use as it will make adding the individual routes way easier/cleaner
def addStats(dict, stats, pos):
    try:
        if pos == 'QB':
            dict['player_name'] = stats.player.full_name
            dict['player_id'] = stats.profile_id
            dict['player_team'] = stats.team
            dict['passing_cmp'] = stats.passing_cmp
            dict['passing_att'] = stats.passing_att
            dict['passing_tds'] = stats.passing_tds
            dict['passing_yds'] = stats.passing_yds
            dict['passing_int'] = stats.passing_int
            dict['passing_sk'] = stats.passing_sk
            dict['rushing_att'] = stats.rushing_att
            dict['rushing_yds'] = stats.rushing_yds
            dict['rushing_tds'] = stats.rushing_tds
        elif pos == 'WR':
            dict['player_name'] = stats.player.full_name
            dict['player_id'] = stats.profile_id
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
            dict['player_id'] = stats.profile_id
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
    except:
        # raise Exception('AddStats failed on player ' + stats.name + ', try updating the player roster')
        return None

# /players/QB/?count={count}&year={year}&week={week}
@app.route('/players/QB/')
def QB():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 5
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    def generate():
        games = nflgame.games(int(year), week=1)
        players = nflgame.combine_game_stats(games)
        playerList = []
        for p in players.passing().sort('passing_yds').limit(int(count)):
            player = addStats({'pos':'QB'}, p, 'QB')
            if player is not None:
                playerList.append(player)
        yield makeResponse(playerList)
    return Response(generate())

# /players/WR/?count={count}&year={year}&week={week}
@app.route('/players/WR/')
def WR():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 5
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    def generate():
        games = nflgame.games(int(year), week=1)
        players = nflgame.combine_game_stats(games)
        playerList = []
        for p in players.receiving().sort('receiving_yds').limit(int(count)):
            if p.guess_position == 'WR':
                player = addStats({'pos':'WR'}, p, 'WR')
                if player is not None:
                    playerList.append(player)
        yield makeResponse(playerList)
    return Response(generate())

# /players/TE/?count={count}&year={year}&week={week}
@app.route('/players/TE/')
def TE():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 5
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    def generate():
        games = nflgame.games(int(year), week=1)
        players = nflgame.combine_game_stats(games)
        playerList = []
        for p in players.receiving().sort('receiving_yds').limit(int(count)):
            if p.guess_position == 'TE':
                player = addStats({'pos':'TE'}, p, 'WR')
                if player is not None:
                    playerList.append(player)
        yield makeResponse(playerList)
    return Response(generate())

# /players/RB/?count={count}&year={year}&week={week}
@app.route('/players/RB/')
def RB():
    count = request.args.get('count')
    year = request.args.get('year')
    week = request.args.get('week')
    if count is None:
        count = 5
    if year is None:
        year = 2018
    if week is not None:
        week = int(week)
    def generate():
        print(datetime.datetime.now())
        games = nflgame.games(int(year), week=10)
        print(datetime.datetime.now())
        players = nflgame.combine_game_stats(games)
        print(datetime.datetime.now())
        playerList = []
        for p in players.rushing().sort('rushing_yds').limit(int(count)):
            player = addStats({'pos':'RB'}, p, 'RB')
            if player is not None:
                playerList.append(player)
        print(datetime.datetime.now())        
        yield makeResponse(playerList)
    return Response(generate())

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
    def generate():
        games = nflgame.games(int(year), week=1)
        players = nflgame.combine_game_stats(games)
        player = nflgame.find(name, team=team)[0]
        for x in players:
            if x.player:
                if x.player.full_name:
                    if x.player.full_name == player.full_name:
                        p = addStats(player.__dict__, x, player.position)
                        if p is not None:
                            p = fillBlanks(p)
                            yield makeResponse([p])
                        break
    return Response(generate())

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=port)  