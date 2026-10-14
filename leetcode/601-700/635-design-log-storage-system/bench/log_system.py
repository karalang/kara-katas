# LeetCode #635: Design Log Storage System -- benchmark, Python.
#
# The ★ arm: timestamps compared as text after cutting them, and the
# bounds, to the granularity's length.

LENGTH = {"Year": 4, "Month": 7, "Day": 10, "Hour": 13, "Minute": 16, "Second": 19}


class LogSystem:
    def __init__(self):
        self.logs = []

    def put(self, log_id, timestamp):
        self.logs.append((log_id, timestamp))

    def retrieve(self, start, end, granularity):
        n = LENGTH.get(granularity, 19)
        low, high = start[:n], end[:n]
        ids = []
        for log_id, timestamp in self.logs:
            cut = timestamp[:n]
            if low <= cut <= high:
                ids.append(log_id)
        return ids


seed = 635


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_time():
    year = 2000 + next_random() % 18
    month = 1 + next_random() % 12
    day = 1 + next_random() % 31
    hour = next_random() % 24
    minute = next_random() % 60
    second = next_random() % 60
    return f"{year}:{month:02}:{day:02}:{hour:02}:{minute:02}:{second:02}"


def main():
    names = ["Year", "Month", "Day", "Hour", "Minute", "Second"]
    logs = LogSystem()
    for log_id in range(1, 20001):
        logs.put(log_id, random_time())
    found = checksum = 0
    for _ in range(2000):
        start = random_time()
        end = random_time()
        granularity = names[next_random() % 6]
        for log_id in logs.retrieve(start, end, granularity):
            found += 1
            checksum = (checksum * 31 + log_id) % 1000000007
    print(f"20000 logs, 2000 retrieves: {found} ids, checksum {checksum}")


main()
