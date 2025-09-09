class Command:
    showCommand: bool
    cmd: str
    args: list[str]

class Item:
    name: str = ""
    type: str = ""
    tags: list[str] = list()
    description: str = ""
    note: str = ""
    url: str = ""
    command: Command = Command()


