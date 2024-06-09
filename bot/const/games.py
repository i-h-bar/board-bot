from bot.game import Game
from games.secret_hitler.game import secret_hitler

GAMES: dict[str, Game] = {
    "Secret Hitler": secret_hitler
}

current_games = set()
