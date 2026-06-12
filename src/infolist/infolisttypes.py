class Command:
    showCommand: bool
    cmd: str
    args: list[str]

class Item:
    name: str = ""
    tags: list[str] = list()
    description: str = ""
    note: str = ""
