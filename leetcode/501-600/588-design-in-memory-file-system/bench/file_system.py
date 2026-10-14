# Benchmark for #588: Python mirror of the ★ arm (a tree of shared
# nodes); see file_system.kara. Each node is an object, and a directory
# keeps its entries in a dict, sorted when it is listed, since Python
# has no sorted map.


class Node:
    __slots__ = ("is_file", "content", "children")

    def __init__(self):
        self.is_file = False
        self.content = ""
        self.children = {}


class FileSystem:
    def __init__(self):
        self.root = Node()

    def walk(self, path, make):
        node = self.root
        for name in path.split("/"):
            if not name:
                continue
            if make and name not in node.children:
                node.children[name] = Node()
            node = node.children[name]
        return node

    def ls(self, path):
        node = self.walk(path, False)
        if node.is_file:
            return [path.split("/")[-1]]
        return sorted(node.children)

    def mkdir(self, path):
        self.walk(path, True)

    def add_content_to_file(self, file_path, content):
        node = self.walk(file_path, True)
        node.is_file = True
        node.content += content

    def read_content_from_file(self, file_path):
        return self.walk(file_path, False).content


# ---- benchmark --------------------------------------------------------------

seed = 588


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def dir_path(depth):
    alphabet = "abcde"
    path = ""
    for _ in range(depth):
        k = next_random() % 5
        path += "/" + alphabet[k]
    return path


def script():
    names = "fghij"
    made = ["/"]
    files = []
    ops = []
    while len(ops) < 300:
        roll = next_random() % 10
        if roll < 3:
            ops.append(("ls", made[next_random() % len(made)], None))
        elif roll < 4 and files:
            ops.append(("read", files[next_random() % len(files)], None))
        elif roll < 7:
            path = dir_path(1 + next_random() % 4)
            made.append(path)
            ops.append(("mkdir", path, None))
        else:
            k = next_random() % 5
            path = dir_path(next_random() % 4) + "/" + names[k]
            content = ""
            for _ in range(1 + next_random() % 5):
                content += names[next_random() % 5]
            made.append(path)
            files.append(path)
            ops.append(("add", path, content))
    return ops


def main():
    count = 200
    rounds = 200
    scripts = [script() for _ in range(count)]
    lines = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            fs = FileSystem()
            for kind, path, content in scripts[(rnd * 7 + g) % count]:
                if kind == "ls":
                    for name in fs.ls(path):
                        checksum = (checksum * 31 + len(name)) % 1000000007
                    lines += 1
                elif kind == "mkdir":
                    fs.mkdir(path)
                elif kind == "add":
                    fs.add_content_to_file(path, content)
                else:
                    checksum = (checksum * 31 + len(fs.read_content_from_file(path))) % 1000000007
                    lines += 1
    print(f"{count} scripts of 300 commands, {rounds} rounds: {lines} answers, checksum {checksum}")


main()
