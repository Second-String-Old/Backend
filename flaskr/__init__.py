import os
import nflgame
import json

from flask import Flask


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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        games = nflgame.games(2018, week=5)
        players = nflgame.combine_game_stats(games)
        retval = []
        for p in players.rushing().sort('rushing_yds').limit(5):
            msg = '%s %d carries for %d yards and %d TDs'
            retval.append(msg % (p, p.rushing_att, p.rushing_yds, p.rushing_tds))
        return makeResponse(retval)
        
    return app