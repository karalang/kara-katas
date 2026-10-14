# LeetCode #635: Design Log Storage System -- Python mirror of the ★ arm.
#
# Timestamps compared as text after cutting them, and the bounds, to the
# granularity's length.

LENGTH = {"Year": 4, "Month": 7, "Day": 10, "Hour": 13, "Minute": 16, "Second": 19}


class LogSystem:
    def __init__(self):
        self.logs = []

    def put(self, log_id, timestamp):
        self.logs.append((log_id, timestamp))

    def retrieve(self, start, end, granularity):
        n = LENGTH.get(granularity, 19)
        low, high = start[:n], end[:n]
        return [i for i, t in self.logs if low <= t[:n] <= high]


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


def show(ids):
    return "[" + ", ".join(str(i) for i in sorted(ids)) + "]"


def ask(logs, start, end, granularity):
    print(f"retrieve({start}, {end}, {granularity}) -> {show(logs.retrieve(start, end, granularity))}")


logs = LogSystem()
logs.put(1, "2017:01:01:23:59:59")
logs.put(2, "2017:01:01:22:59:59")
logs.put(3, "2016:01:01:00:00:00")
ask(logs, "2016:01:01:01:01:01", "2017:01:01:23:00:00", "Year")
ask(logs, "2016:01:01:01:01:01", "2017:01:01:23:00:00", "Hour")
logs.put(4, "2017:01:01:22:59:59")
logs.put(5, "2016:12:31:23:59:59")
ask(logs, "2017:01:01:22:59:59", "2017:01:01:22:59:59", "Second")
ask(logs, "2016:12:31:23:59:59", "2016:12:31:23:59:59", "Minute")
ask(logs, "2017:01:01:22:00:00", "2017:01:01:22:00:00", "Hour")
ask(logs, "2016:12:31:00:00:00", "2017:01:01:00:00:00", "Day")
ask(logs, "2016:12:01:00:00:00", "2016:12:31:00:00:00", "Month")
ask(logs, "2017:01:01:23:00:00", "2016:01:01:00:00:00", "Year")
ask(logs, "2016:12:31:23:59:59", "2017:01:01:00:00:00", "Second")
names = ["Year", "Month", "Day", "Hour", "Minute", "Second"]
sheet = LogSystem()
for i in range(1, 301):
    sheet.put(i, random_time())
found = checksum = 0
for _ in range(200):
    start = random_time()
    end = random_time()
    granularity = names[next_random() % 6]
    for i in sorted(sheet.retrieve(start, end, granularity)):
        found += 1
        checksum = (checksum * 31 + i) % 1000000007
print(f"300 logs, 200 retrieves: {found} ids, checksum {checksum}")
