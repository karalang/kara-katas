# LeetCode #588: Design In-Memory File System -- Python mirror of the ★
# arm (a tree of shared nodes); see file_system.kara. A directory keeps
# its entries in a dict, sorted when it is listed, since Python has no
# sorted map.


class Node:
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


# ---- test harness -----------------------------------------------------------

seed = 588


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def run(fs, command):
    kind = command[0]
    if kind == "ls":
        return "[" + " ".join(fs.ls(command[1])) + "]"
    if kind == "mkdir":
        fs.mkdir(command[1])
        return None
    if kind == "add":
        fs.add_content_to_file(command[1], command[2])
        return None
    return fs.read_content_from_file(command[1])


def run_all(commands):
    fs = FileSystem()
    printed = []
    for command in commands:
        out = run(fs, command)
        if out is not None:
            printed.append(out)
    return printed


def show(name, commands):
    print(f"{name}: {' '.join(run_all(commands))}")


def ls(path):
    return ("ls", path)


def mkdir(path):
    return ("mkdir", path)


def add(path, content):
    return ("add", path, content)


def read(path):
    return ("read", path)


def script(count, letters, depth):
    alphabet = "abcdefghij"
    files = set()
    dirs = set()
    made = ["/"]
    commands = []
    while len(commands) < count:
        roll = step() % 10
        if roll < 4:
            path = made[step() % len(made)]
            if roll < 2 or path not in files:
                commands.append(("ls", path))
            else:
                commands.append(("read", path))
            continue
        is_file = roll >= 7
        length = 1 + step() % depth
        steps = []
        path = ""
        ok = True
        for i in range(length):
            k = step() % letters
            path += "/" + alphabet[k]
            last = i == length - 1
            if path in files and not (last and is_file):
                ok = False
            if path in dirs and last and is_file:
                ok = False
            steps.append(path)
        if not ok:
            continue
        if is_file:
            content = ""
            for _ in range(1 + step() % 3):
                content += alphabet[step() % letters]
            commands.append(("add", path, content))
        else:
            commands.append(("mkdir", path))
        for i in range(len(steps)):
            is_new = steps[i] not in files and steps[i] not in dirs
            if i == len(steps) - 1 and is_file:
                files.add(steps[i])
            else:
                dirs.add(steps[i])
            if is_new:
                made.append(steps[i])
    return commands


def checksum_of(printed):
    checksum = 0
    for line in printed:
        for b in line.encode():
            checksum = (checksum * 131 + b) % 1000000007
        checksum = (checksum * 131 + 10) % 1000000007
    return checksum


def main():
    show("example", [ls("/"), mkdir("/a/b/c"), add("/a/b/c/d", "hello"), ls("/"), read("/a/b/c/d")])
    show("empty", [ls("/")])
    show("file at the root", [add("/f", "abc"), ls("/"), read("/f")])
    show("a file listed", [add("/a/b", "x"), ls("/a/b")])
    show("added twice", [add("/f", "ab"), add("/f", "cd"), read("/f"), add("/f", "e"), read("/f")])
    show("in order", [mkdir("/c"), mkdir("/a"), add("/b", "x"), mkdir("/aa"), ls("/")])
    show("deep", [mkdir("/a/b/c/d/e/f/g"), ls("/a/b/c/d/e/f"), ls("/a/b/c/d/e/f/g"), ls("/a")])
    show("side by side", [mkdir("/d/x"), add("/d/y", "y"), add("/d/x/z", "z"), ls("/d"), ls("/d/x"), read("/d/x/z"), ls("/d/y")])
    total = 0
    checksum = 0
    for _ in range(300):
        count = 1 + step() % 40
        letters = 2 + step() % 3
        printed = run_all(script(count, letters, 4))
        total += len(printed)
        checksum = (checksum * 31 + checksum_of(printed)) % 1000000007
    print(f"300 random scripts: {total} lines printed, checksum {checksum}")
    wide = run_all(script(300, 10, 3))
    print(f"300 commands over ten names: {len(wide)} lines printed, checksum {checksum_of(wide)}")
    deep = run_all(script(300, 2, 30))
    print(f"300 commands, 30 deep: {len(deep)} lines printed, checksum {checksum_of(deep)}")


main()
