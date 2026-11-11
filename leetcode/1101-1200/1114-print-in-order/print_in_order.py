# LeetCode #1114: Print in Order -- mirrors the ★ arm: a thread per
# method and two `threading.Event`s as its two one-shot channels, the log
# behind a lock.
import threading


class Foo:
    def __init__(self):
        self.first_done = threading.Event()
        self.second_done = threading.Event()

    def first(self, print_first):
        print_first()
        self.first_done.set()

    def second(self, print_second):
        self.first_done.wait()
        print_second()
        self.second_done.set()

    def third(self, print_third):
        self.second_done.wait()
        print_third()


def run(nums):
    lock = threading.Lock()
    log = []

    def write(word):
        def p():
            with lock:
                log.append(word)
        return p

    foo = Foo()
    threads = []
    for k in nums:
        if k == 1:
            t = threading.Thread(target=foo.first, args=(write("first"),))
        elif k == 2:
            t = threading.Thread(target=foo.second, args=(write("second"),))
        else:
            t = threading.Thread(target=foo.third, args=(write("third"),))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return "".join(log)


state = [1114]


def next_random():
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def show(nums):
    return "[" + ", ".join(str(k) for k in nums) + "]"


orders = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
for nums in orders:
    print(f"{show(nums)} -> {run(nums)}")
in_order = 0
check = 0
for _ in range(2000):
    out = run(orders[next_random() % 6])
    if out == "firstsecondthird":
        in_order += 1
    for b in out.encode():
        check = (check * 131 + b) % 1000000007
print(f"2000 runs in random orders: {in_order} printed in order, checksum {check}")
