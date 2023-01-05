class SimultaneousQueryError(Exception):
    def __init__(self, *content):
        self.content = content

    def __str__(self):
        return f"Simultaneous queried {self.content[0]} and {self.content[1]}"


class CharacterNameError(Exception):
    def __init__(self, content: list):
        self.content = content

    def __str__(self):
        return f"The name of the character is incorrect: {', '.join(self.content)}"


class ElementError(Exception):
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return f"The element of the character is wrong:{self.content}"


class OutOfSpecificationError(Exception):
    def __init__(self, *content):
        self.content = content

    def __str__(self):
        return f"Incoming level or constellation seat is out of regulation:" \
               f"{self.content[0]}--{self.content[1]} ({'constellation' if self.content[2] else 'level'})"
