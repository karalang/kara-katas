# The values every format job can name, shared by mk.py's checks and oracle.py.


class User:
    def __init__(self, name, id, email, tags):
        self.name = name
        self.id = id
        self.email = email
        self.tags = tags

    def __repr__(self):
        return "User(%r, %d)" % (self.name, self.id)

    def __str__(self):
        return "%s <%s>" % (self.name, self.email)


def keywords():
    return {
        "name": "Ada Lovelace",
        "city": "Zürich",
        "quote": "it's \"fine\"\n\ttab",
        "empty": "",
        "n": 1234567,
        "neg": -42,
        "zero": 0,
        "w": 12,
        "p": 3,
        "ch": 233,
        "emoji": 128512,
        "big": 12345678901234567,
        "u": User("ada", 7, "ada@example.com", ["admin", "ops"]),
        "cfg": {"host": "db1", "port": 5432, "users": ["ada", "bob"], "1": "one"},
        "nums": [3, 1, 4, 1, 5],
        "fill": "*",
        "align": "^",
        "r125": 125,
        "r135": 135,
        "r6": 999999,
        "r7": 9999995,
    }
