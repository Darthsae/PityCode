import random
from enum import Enum
from typing import Callable

def intput(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except Exception as e:
            continue

class Relation(Enum):
    BEFORE = 0
    AFTER = 0

class Loadable:
    def __init__(self, name: str, loadRules: dict[Relation]) -> None:
        self.name = name
        self.loadRules = loadRules

class Loader:
    def __init__(self) -> None:
        self.loaded: list[Loadable] = []

class Option:
    def __init__(self, name: str, description: str, function: Callable[tuple[None], None]) -> None:
        self.name = name
        self.description = description
        self.function = function

class Menu:
    def __init__(self, name: str, options: list[Option]) -> None:
        self.name = name
        self.options = options

    def display(self, displayFunction: Callable[tuple[int, Option], None]) -> None:
        map(displayFunction, enumerate(self.options))

class App:
    def __init__(self, name: str) -> None:
        self.name = name
        self.quit = False

    def run(self) -> None:
        """Run the main loop of the application for one cycle.
        """
        choice: int = intput("Option: ") - 1

        match choice:
            case 0:
                print("Zero")
            case 1:
                print("One")

app: App = App("Test")

menuOne: Menu = Menu("Ya", [Option(f"{i}", "", lambda: None) for i in range(20)])

menuOne.display(lambda i, x: print(f"{i}. {x.name}"))

while not app.quit:
    app.run()
