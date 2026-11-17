# LeetCode #1600: Throne Inheritance -- mirrors throne.kara: children in
# a dict of lists, the dead in a set, the preorder walked with a stack.


class ThroneInheritance:
    def __init__(self, king_name):
        self.king = king_name
        self.children = {}
        self.dead = set()

    def birth(self, parent_name, child_name):
        self.children.setdefault(parent_name, []).append(child_name)

    def death(self, name):
        self.dead.add(name)

    def get_inheritance_order(self):
        order = []
        stack = [self.king]
        while stack:
            name = stack.pop()
            if name not in self.dead:
                order.append(name)
            stack.extend(reversed(self.children.get(name, [])))
        return order


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def mix_order(check, order):
    c = check
    for name in order:
        for b in name.encode():
            c = (c * 31 + b + 1) % 1000000007
        c = (c * 31 + 7) % 1000000007
    return c


def reign(steps, seed):
    throne = ThroneInheritance("king")
    alive = ["king"]
    born = 0
    check = 0
    asked = 0
    for _ in range(steps):
        r = next_random(seed) % 8
        if r < 4 and alive:
            parent = alive[next_random(seed) % len(alive)]
            born += 1
            child = f"p{born}"
            throne.birth(parent, child)
            alive.append(child)
        elif r == 4 and alive:
            at = next_random(seed) % len(alive)
            alive[at], alive[-1] = alive[-1], alive[at]
            name = alive.pop()
            throne.death(name)
        else:
            check = mix_order(check, throne.get_inheritance_order())
            asked += 1
    check = mix_order(check, throne.get_inheritance_order())
    return check, asked + 1


def batch(count, most, seed):
    check = 0
    asked = 0
    for _ in range(count):
        steps = next_random(seed) % most + 1
        c, a = reign(steps, seed)
        check = (check * 31 + c) % 1000000007
        asked += a
    print(f"{count} reigns of up to {most} calls: {asked} orders, checksum {check}")


def show(order):
    return "[" + ", ".join(order) + "]"


def main():
    throne = ThroneInheritance("king")
    for p, c in [("king", "andy"), ("king", "bob"), ("king", "catherine"), ("andy", "matthew"), ("bob", "alexander"), ("bob", "asha")]:
        throne.birth(p, c)
    print(show(throne.get_inheritance_order()))
    throne.death("bob")
    print(show(throne.get_inheritance_order()))
    throne.death("king")
    throne.birth("asha", "zoe")
    print(show(throne.get_inheritance_order()))
    seed = [1600]
    batch(3000, 10, seed)
    batch(300, 200, seed)
    batch(3, 5000, seed)


main()
