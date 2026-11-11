# LeetCode #1115: Print FooBar Alternately -- mirrors the ★ arm: two
# one-slot queues hold the turns, foo's filled when the pair is made.
import threading
import queue


class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_turn = queue.Queue(1)
        self.bar_turn = queue.Queue(1)
        self.foo_turn.put(())

    def foo(self, print_foo):
        for _ in range(self.n):
            self.foo_turn.get()
            print_foo()
            self.bar_turn.put(())

    def bar(self, print_bar):
        for _ in range(self.n):
            self.bar_turn.get()
            print_bar()
            self.foo_turn.put(())


state = [1115]


def next_random():
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def run(n, bar_first):
    log = []
    lock = threading.Lock()

    def say(s):
        with lock:
            log.append(s)

    fb = FooBar(n)
    a = threading.Thread(target=fb.foo, args=(lambda: say("foo"),))
    b = threading.Thread(target=fb.bar, args=(lambda: say("bar"),))
    ts = [b, a] if bar_first else [a, b]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return "".join(log)


def checksum(s, check=0):
    for b in s.encode():
        check = (check * 131 + b) % 1000000007
    return check


def yes(b):
    return "true" if b else "false"


print(f"n = 1 -> {run(1, False)}")
print(f"n = 2 -> {run(2, False)}")
print(f"n = 2, bar started first -> {run(2, True)}")
print(f"n = 3, bar started first -> {run(3, True)}")
alternating = 0
check = 0
for _ in range(2000):
    n = next_random() % 12 + 1
    bar_first = next_random() % 2 == 1
    out = run(n, bar_first)
    if out == "foobar" * n:
        alternating += 1
    check = checksum(out, check)
print(f"2000 runs of up to 12 rounds: {alternating} alternating, checksum {check}")
out = run(1000, True)
print(f"n = 1000: {len(out)} characters, alternating {yes(out == 'foobar' * 1000)}, checksum {checksum(out)}")
