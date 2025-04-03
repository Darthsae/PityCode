import random
from typing import TypeAlias, Callable
from enum import Enum

class Operation(Enum):
    Add = 0
    Multiply = 1

Modifier: TypeAlias = tuple[Operation, str, float]

Stat: TypeAlias = tuple[str, int]
EntityConsumer: TypeAlias = Callable[tuple["Entity"], ...]

class StatusType:
    def __init__(self, name: str, description: str, duration: int, onApply: EntityConsumer, onTick: EntityConsumer, onRemove: EntityConsumer) -> None:
        self.name = name
        self.description = description
        self.duration = duration
        self.onApply = onApply
        self.onTick = onTick
        self.onRemove = onRemove

class StatusInstance:
    def __init__(self, statusType: StatusType) -> None:
        """An instance of a status.

        Args:
            statusType (int): The status type.
        """
        self.type = statusType
        self.duration = statusType.duration

    def onTick(self, entity: "Entity"):
        self.type.onTick(entity)
        self.duration -= 1
        if self.duration <= 0:
            self.type.onRemove(entity)
            return False
        return True


class Perk:
    def __init__(self, name: str, description: str, modifiers: list[Modifier]) -> None:
        self.name = name
        self.description = description
        self.modifiers = modifiers

class Trait:
    def __init__(self, name: str, description: str, modifiers: list[Modifier]) -> None:
        self.name = name
        self.description = description
        self.modifiers = modifiers

class EntityType:
    def __init__(self, name: str, description: str, stats: list[Stat]) -> None:
        self.name = name
        self.description = description
        self.stats = stats

class Entity:
    def __init__(self, name: str, entityType: EntityType) -> None:
        self.name = name
        self.type = entityType
        self.stats = entityType.stats
        self.perks: list[Perk] = []
        self.traits: list[Trait] = []
        self.statuses: list[StatusInstance] = []

    def applyStatus(self, statusType: StatusType) -> None:
        temp: StatusInstance = StatusInstance(statusType)
        self.statuses.append(temp)
        temp.type.onApply(self)

    def onTick(self) -> None:
        toRemove: list[int] = []

        for i, status in enumerate(self.statuses):
            if not status.onTick(self):
                toRemove.append(i)

        for index in reversed(toRemove):
            self.statuses.pop(index)

    def recalculate(self) -> None:
        self.stats = self.type.stats
        multipliers: dict[str, float] = {}
        modifiers: list[Modifier] = []
        
        for perk in self.perks:
            print(perk.modifiers)
            modifiers.extend(perk.modifiers)

        for trait in self.traits:
            modifiers.extend(trait.modifiers)
        
        for modifier in modifiers:
            match modifier[0]:
                case Operation.Add:
                    for i, stat in enumerate(self.stats):
                        if stat[0] == modifier[1]:
                            self.stats[i] = (stat[0], stat[1] + modifier[2])
                            break
                        self.stats.append((modifier[1], modifier[2]))
                case Operation.Multiply:
                    multipliers[modifier[1]] = multipliers.get(modifier[1], 1) * modifier[2]
       
        print(multipliers)

        for statName, multiplier in multipliers.items():
            for i, stat in enumerate(self.stats):
                if stat[0] == statName:
                    self.stats[i] = (stat[0], stat[1] * multiplier)
                    break

baseStats: list[Stat] = [("life", 10)]

entityTypes: list[EntityType] = [EntityType("Grug", "A grug.", baseStats)]
grog: Entity = Entity("Grog", entityTypes[0])
perk: Perk = Perk("a", "A perk.", [(Operation.Multiply, "life", 2.5)])
grog.perks.append(perk)
grog.recalculate()
print(grog.stats)
