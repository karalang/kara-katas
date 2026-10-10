# LeetCode #359: Logger Rate Limiter -- mirror of logger.kara.


class Logger:
    def __init__(self):
        self.next_ok = {}

    def should_print_message(self, timestamp, message):
        t = self.next_ok.get(message)
        if t is not None and timestamp < t:
            return False
        self.next_ok[message] = timestamp + 10
        return True


def run(label, calls):
    logger = Logger()
    line = "".join("T" if logger.should_print_message(t, m) else "F" for t, m in calls)
    print(f"{label}: {line}")


def main():
    run("example", [(1, "foo"), (2, "bar"), (3, "foo"), (8, "bar"), (10, "foo"), (11, "foo")])

    run("no calls", [])
    run("one message once", [(0, "a")])
    run("exactly ten seconds later", [(0, "a"), (10, "a")])
    run("nine seconds later", [(0, "a"), (9, "a")])
    run("same timestamp twice", [(5, "a"), (5, "a")])
    run("refusals do not reset the clock", [(0, "a"), (5, "a"), (9, "a"), (10, "a"), (19, "a"), (20, "a")])
    run("messages are independent", [(0, "a"), (1, "b"), (2, "a"), (3, "b"), (10, "a"), (11, "b")])
    run("empty message", [(0, ""), (3, ""), (10, "")])
    run("prefixes are different messages", [(0, "ab"), (1, "a"), (2, "abc"), (3, "ab")])
    run("large timestamps", [(1000000000, "x"), (1000000009, "x"), (1000000010, "x")])

    seed = 359
    logger = Logger()
    t = 0
    printed = 0
    checksum = 0
    for _ in range(20000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        t += (seed // 65536) % 4
        seed = (seed * 1103515245 + 12345) % 2147483648
        mid = (seed // 65536) % 50
        ok = logger.should_print_message(t, f"msg{mid}")
        if ok:
            printed += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"20000 random calls: {printed} printed, checksum {checksum}")


main()
