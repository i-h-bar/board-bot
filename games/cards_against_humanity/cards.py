import random
from dataclasses import dataclass
from pathlib import Path
from typing import Self

WHITE_CARDS = Path("games/cards_against_humanity/assets/white.txt")
BLACK_CARDS = Path("games/cards_against_humanity/assets/black.txt")


@dataclass(slots=True, frozen=True, repr=True)
class WhiteCard:
    text: str


@dataclass(slots=True, frozen=True, repr=True)
class BlackCard:
    text: str
    slots: int


class Deck[T]:
    __slots__ = ("cards", "discard_pile", "card_type")

    def __init__(self, cards: list[T]):
        self.cards = cards
        self.discard_pile: list[T] = []
        self.card_type = type(self.cards[0])
        random.shuffle(self.cards)

    def __repr__(self: Self) -> str:
        return f"{self.__class__.__name__}({self.card_type.__name__}, len={len(self.cards) + len(self.discard_pile)})"

    @classmethod
    def white(cls: type[Self]) -> Self:
        return cls([WhiteCard(text) for text in WHITE_CARDS.read_text().splitlines()])

    @classmethod
    def black(cls: type[Self]) -> Self:
        return cls([BlackCard(text=text, slots=text.count("{}") or 1) for text in BLACK_CARDS.read_text().splitlines()])

    def draw(self: Self) -> T:
        if not self.cards:
            self.reset()

        card = self.cards.pop()
        return card

    def reset(self: Self) -> None:
        self.cards = self.discard_pile
        self.discard_pile = []
        random.shuffle(self.cards)

    def discard(self: Self, card: T) -> None:
        self.discard_pile.append(card)
