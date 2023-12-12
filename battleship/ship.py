from enum import Enum
from typing import Set


class ShipStatus(Enum):
    NEW = 0
    HIT = 1
    SUNK = 2


class Ship:
    def __init__(self, name: str, shipsize: int) -> None:
        self.name: str = name
        self.size: int = shipsize
        self.status: ShipStatus = ShipStatus.NEW
        self.positions: Set[str] = set()
        self.hits: Set[str] = set()
    
    def missile(self, position: str) -> str:
        if position in self.positions:
            self.hits.add(position)
            if self.positions.difference(self.hits):
                self.status = ShipStatus.HIT
                return "hit"
            else:
                self.status = ShipStatus.SUNK
                return "sunk " + self.name
        else:
            return "miss"
