from games.interface import Game
from games.secret_hitler.game import secret_hitler

GAMES: dict[str, Game] = {
    secret_hitler.name: secret_hitler
}

current_games = set()
