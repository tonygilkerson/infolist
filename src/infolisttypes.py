class Command:
    showCommand: bool
    cmd: str
    args: list[str]

class Item:
    name: str
    type: str
    description: str
    note: str
    url: str
    command: Command


