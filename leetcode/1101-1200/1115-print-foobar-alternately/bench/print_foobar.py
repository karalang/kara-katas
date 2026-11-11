# LeetCode #1115: Print FooBar Alternately -- the bench's Python mirror:
# a thread per method and two `threading.Semaphore`s as the ★ arm's two
# turn channels, foo's holding one permit; the log behind a lock.
import threading


class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_turn = threading.Semaphore(1)
        self.bar_turn = threading.Semaphore(0)

    def foo(self, print_foo):
        for _ in range(self.n):
            self.foo_turn.acquire()
            print_foo()
            self.bar_turn.release()

    def bar(self, print_bar):
        for _ in range(self.n):
            self.bar_turn.acquire()
            print_bar()
            self.foo_turn.release()


def run(n, bar_first):
    lock = threading.Lock()
    log = []

    def write(word):
        def p():
            with lock:
                log.append(word)
        return p

    fb = FooBar(n)
    a = threading.Thread(target=fb.foo, args=(write("foo"),))
    b = threading.Thread(target=fb.bar, args=(write("bar"),))
    ts = [b, a] if bar_first else [a, b]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return "".join(log)


def main():
    want = "foobar" * 200
    alternating = 0
    check = 0
    for r in range(1000):
        out = run(200, r % 2 == 1)
        if out == want:
            alternating += 1
        check = (check * 31 + len(out) + r) % 1000000007
    print(f"1000 runs of 200 rounds: {alternating} alternating, checksum {check}")


main()
