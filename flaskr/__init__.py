import os
import nflgame
import json

from flask import Flask
from flask import request

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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
        count = int(request.args.get('count'))
        year = int(request.args.get('year'))
        week = int(request.args.get('week'))
        if count is None:
            count = 25
        if year is None:
            year = 2018
        games = nflgame.games(year, week=week)
        players = nflgame.combine_game_stats(games)
        qbPL = []
        for p in players.passing().sort('passing_yds').limit(count):
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
            qbPL.append(player)
        return makeResponse(qbPL)
    return app