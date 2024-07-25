from games.interface import Game
from games.secret_hitler.game import secret_hitler
from games.cards_against_humanity.game import cah

GAMES: dict[str, Game] = {
    secret_hitler.name: secret_hitler,
    cah.name: cah
}

current_games = set()
