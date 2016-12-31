#!/usr/bin/env python

"""A server to manage Kabou games."""

from flask import Flask, request
from flask.ext.jsonpify import jsonify
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy import ForeignKeyConstraint
from werkzeug import generate_password_hash  # , check_password_hash
# from flask.ext.restful import Api, Resource

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

app = Flask(__name__)

# SQLalchemy stuff
engine = create_engine('sqlite:///kabou_data.db', echo=True)
Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(54))

    def __init__(self, password):
        self.password = generate_password_hash(password)
        self.rounds = []
        self.players = []

    def add_player(self, player):
        """
        Add a player to the current game.

        Once a game is started (e.g. the first round began) no new player may
        join.

        Parameters
        ----------
        player : Player object
        """
        if len(self.rounds) == 0:
            self.players.append(player)
        else:
            return jsonify({'error': 'Game already started.'})

    def start_round(self):
        if len(self.players) < 2:
            return jsonify({'error': 'Each game has to have at least '
                                     '2 players.'})
        self.rounds.append(Round(self.players))

    def get_dict(self):
        return {'id': str(self.id),
                'password': self.password,
                'rounds': self.rounds,
                'players': self.players}


class Round(Base):
    """A round belongs to a game."""

    __tablename__ = 'rounds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    current_player_id = Column(Integer, ForeignKey('players.id'))

    def __init__(self, players, starting_player):
        self.players = players
        self.current_player = players[starting_player].id


class Player(Base):
    """Represents a player of Kabou. This might be an A.I. or a human."""

    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    password = Column(String(54))

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)

    def get_dict(self):
        return {'id': self.id, 'name': self.name}


class PlayerInGame(Base):
    """Say which players are in which game."""

    __tablename__ = 'player_in_game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    game_id = Column(Integer, ForeignKey('games.id'))

    # __table_args__ = (
    #     ForeignKeyConstraint(
    #         ['player_id', 'game_id'],
    #         ['players.id', 'games.id'],
    #         name="fk_games_players"),
    # )


@app.route('/api/v1.0/player', methods=['GET'])
def get_players():
    players = session.query(Player)
    return jsonify({'players': [ob.get_dict() for ob in players]})


@app.route('/api/v1.0/player', methods=['POST'])
def create_player():
    if request.form and 'password' in request.form and 'name' in request.form:
        name = request.form['name']
        password = request.form['password']
    elif (request.json and 'password' in request.json and
          'name' in request.json):
        name = request.json['name']
        password = request.json['password']
    else:
        return jsonify({'error': '"name" and "password" '
                                 'have to be specified.'})

    player = Player(name=name, password=password)
    try:
        session.add(player)
        session.commit()
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'player already exists.'})
    return jsonify(player.get_dict())


@app.route('/api/v1.0/game', methods=['POST'])
def create_game():
    if request.form and 'password' in request.form:
        password = request.form['password']
    elif request.json and 'password' in request.json:
        password = request.json['password']
    else:
        password = None
    game = Game(password)
    session.add(game)
    session.commit()
    return jsonify(game.get_dict())


@app.route('/api/v1.0/game', methods=['GET'])
def get_games():
    games = session.query(Game)
    return jsonify({'games': [ob.get_dict() for ob in games]})


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    app.run(debug=True)
