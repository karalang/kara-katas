# LeetCode #1600: Throne Inheritance
# -- the bench in Python, mirroring throne.kara: children in a dict of
# lists, the dead in a set, the preorder walked with a stack, through 10
# reigns of 50000 calls, drawn first.


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
            kids = self.children.get(name)
            if kids:
                stack.extend(reversed(kids))
        return order


def main():
    seed = 1600

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    reigns = []
    for _ in range(10):
        alive = ["king"]
        born = 0
        ops = []
        for _ in range(50000):
            r = next_random() % 1000
            if r < 500 and alive:
                parent = alive[next_random() % len(alive)]
                born += 1
                child = f"p{born}"
                ops.append((0, parent, child))
                alive.append(child)
            elif r < 625 and alive:
                at = next_random() % len(alive)
                alive[at], alive[-1] = alive[-1], alive[at]
                ops.append((1, alive.pop(), None))
            elif r < 626:
                ops.append((2, None, None))
        reigns.append(ops)
    check = 0
    names = 0
    for ops in reigns:
        throne = ThroneInheritance("king")
        for kind, a, b in ops:
            if kind == 0:
                throne.birth(a, b)
            elif kind == 1:
                throne.death(a)
            else:
                order = throne.get_inheritance_order()
                names += len(order)
                for name in order:
                    check = (check * 31 + len(name) + 1) % 1000000007
    print(f"10 reigns of 50000 calls: {names} names in the orders, checksum {check}")


main()
