import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

_WHITE_CARDS = Path("games/cards_against_humanity/assets/white.txt")
_BLACK_CARDS = Path("games/cards_against_humanity/assets/black.txt")


@dataclass(slots=True, frozen=True, repr=True)
class WhiteCard:
    text: str


@dataclass(slots=True, frozen=True, repr=True)
class BlackCard:
    text: str
    slots: int


class Deck[T]:
    __slots__ = ("cards", "discard", "card_type")

    def __init__(self, cards: list[T]):
        self.cards = cards
        self.discard: list[T] = []
        self.card_type = type(self.cards[0])
        random.shuffle(self.cards)

    def __repr__(self: Self) -> str:
        return f"{self.__class__.__name__}({self.card_type.__name__}, len={len(self.cards) + len(self.discard)})"

    @classmethod
    def white(cls: type[Self]) -> Self:
        return cls([WhiteCard(text) for text in _WHITE_CARDS.read_text().splitlines()])

    @classmethod
    def black(cls: type[Self]) -> Self:
        return cls([BlackCard(text=text, slots=text.count("____")) for text in _BLACK_CARDS.read_text().splitlines()])

    def draw(self: Self) -> T:
        if not self.cards:
            self.reset()

        card = self.cards.pop()
        return card

    def reset(self: Self) -> None:
        self.cards = self.discard
        random.shuffle(self.cards)
        self.discard = []

    def discard(self: Self, card: T) -> None:
        self.discard.append(card)
