from games.interface import Game
from games.cards_against_humanity.game import cah

GAMES: dict[str, Game] = {
    # secret_hitler.name: secret_hitler,
    cah.name: cah
}

current_games = set()
