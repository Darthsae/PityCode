import random
from enum import Enum

def intput(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except e:
            continue

class Relation(Enum):
    BEFORE = 0
    AFTER = 0

class Loadable:
    def __init__(self, name: str, loadRules: dict[Relation] = {}) -> None:
        self.name = name
        self.loadRules = loadRules

class Loader:
    def __init__(self) -> None:
        self.loaded: list[Loadable] = []

class Menu:
    def __init__(self, name: str) -> None:
        self.name = name

class App:
    def __init__(self, name: str) -> None:
        self.name = name
        self.quit = False

    def run(self) -> None:
        """Run the main loop of the application for one cycle.
        """
        choice: int = intput("Option: ")

app: App = App("Test")

while not app.quit:
app.run()
