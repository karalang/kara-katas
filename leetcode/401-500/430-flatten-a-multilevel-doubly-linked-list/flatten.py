# LeetCode #430: Flatten a Multilevel Doubly Linked List -- mirror of
# flatten.kara (recursion).


class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None
        self.child = None


def flatten_level(head):
    cur = head
    while True:
        after = cur.next
        if cur.child is not None:
            c = cur.child
            child_tail = flatten_level(c)
            cur.next = c
            c.prev = cur
            cur.child = None
            if after is not None:
                child_tail.next = after
                after.prev = child_tail
            else:
                return child_tail
        if after is not None:
            cur = after
        else:
            return cur


def flatten(head):
    if head is None:
        return None
    flatten_level(head)
    return head


# ---- test harness ---------------------------------------------------------


def parse(text, at):
    head = None
    last = None
    while at[0] < len(text) and text[at[0]] != ")":
        if text[at[0]] == " ":
            at[0] += 1
            continue
        negative = False
        if text[at[0]] == "-":
            negative = True
            at[0] += 1
        val = 0
        while at[0] < len(text) and text[at[0]].isdigit():
            val = val * 10 + int(text[at[0]])
            at[0] += 1
        if negative:
            val = -val
        node = Node(val)
        if at[0] < len(text) and text[at[0]] == "(":
            at[0] += 1
            node.child = parse(text, at)
            at[0] += 1
        if last is not None:
            last.next = node
            node.prev = last
        else:
            head = node
        last = node
    return head


def read(head):
    forward = []
    ok = True
    tail = None
    cur = head
    while cur is not None:
        forward.append(cur.val)
        if cur.child is not None:
            ok = False
        if cur.next is not None:
            if cur.next.prev is None or cur.next.prev.val != cur.val:
                ok = False
        else:
            tail = cur
        cur = cur.next
    backward = 0
    cur = tail
    while cur is not None:
        if backward >= len(forward) or forward[len(forward) - 1 - backward] != cur.val:
            ok = False
        backward += 1
        cur = cur.prev
    if backward != len(forward):
        ok = False
    return "[" + " ".join(str(v) for v in forward) + "]" + ("" if ok else " BROKEN")


def show(text):
    head = parse(text, [0])
    print(f"{text} -> {read(flatten(head))}")


seed = 430


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(budget, depth, next_val):
    out = []
    length = 1 + step() % 5
    for i in range(length):
        if budget[0] == 0:
            break
        budget[0] -= 1
        if i > 0:
            out.append(" ")
        out.append(str(next_val[0]))
        next_val[0] += 1
        if depth < 6 and budget[0] > 0 and step() % 4 == 0:
            out.append("(")
            out.append(random_text(budget, depth + 1, next_val))
            out.append(")")
    return "".join(out)


def main():
    show("1 2 3(7 8(11 12) 9 10) 4 5 6")
    show("1(3) 2")
    show("")
    show("1")
    show("1(2(3(4(5))))")
    show("1 2 3 4(5 6 7)")
    show("1(2) 3(4) 5(6)")
    show("-5 0(-1(-2) 7) 9")
    nodes = 0
    checksum = 0
    for _ in range(300):
        budget = [step() % 51]
        next_val = [1]
        text = "" if budget[0] == 0 else random_text(budget, 0, next_val)
        line = read(flatten(parse(text, [0])))
        nodes += next_val[0] - 1
        for b in line.encode():
            checksum = (checksum * 31 + b) % 1000000007
    print(f"300 random lists, {nodes} nodes: checksum {checksum}")


main()
