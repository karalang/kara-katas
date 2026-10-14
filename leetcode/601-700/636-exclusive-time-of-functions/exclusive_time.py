# LeetCode #636: Exclusive Time of Functions -- Python mirror of the ★ arm.
#
# One stack of running functions and the time of the last event.


def exclusive_time(n, logs):
    total = [0] * n
    stack = []
    prev = 0
    for log in logs:
        parts = log.split(":")
        fid = int(parts[0])
        t = int(parts[2])
        if parts[1] == "start":
            if stack:
                total[stack[-1]] += t - prev
            stack.append(fid)
            prev = t
        else:
            top = stack.pop()
            total[top] += t - prev + 1
            prev = t + 1
    return total


seed = 636


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def random_logs(n, calls, gap):
    logs = []
    stack = []
    started = 0
    start_at = end_at = 0
    while started < calls or stack:
        begin = started < calls and (not stack or next_random() % 2 == 0)
        if begin:
            fid = next_random() % n
            t = start_at + wide() % gap
            logs.append(f"{fid}:start:{t}")
            stack.append(fid)
            started += 1
            start_at = t + 1
            end_at = t
        else:
            fid = stack.pop()
            t = end_at + wide() % gap
            logs.append(f"{fid}:end:{t}")
            start_at = end_at = t + 1
    return logs


def show(times):
    return "[" + ", ".join(str(t) for t in times) + "]"


def ask(n, logs):
    print(f"n = {n}, {len(logs)} logs -> {show(exclusive_time(n, logs))}")


ask(2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"])
ask(1, ["0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7"])
ask(2, ["0:start:0", "0:start:2", "0:end:5", "1:start:6", "1:end:6", "0:end:7"])
ask(1, ["0:start:0", "0:end:0"])
ask(2, ["0:start:0", "0:end:3", "1:start:4", "1:end:4"])
ask(2, ["1:start:5", "1:end:9"])
ask(2, ["0:start:0", "1:start:1", "1:end:8", "0:end:9"])
ask(3, ["0:start:0", "1:start:1", "2:start:2", "2:end:2", "1:end:3", "0:end:4"])
ask(2, ["0:start:0", "1:start:999999998", "1:end:999999999", "0:end:1000000000"])
total = checksum = 0
for _ in range(300):
    n = 1 + next_random() % 5
    calls = 1 + next_random() % 20
    for t in exclusive_time(n, random_logs(n, calls, 4)):
        total += t
        checksum = (checksum * 31 + t) % 1000000007
print(f"300 random cases: total {total}, checksum {checksum}")
logs = random_logs(100, 250, 3800000)
times = exclusive_time(100, logs)
most = 0
for i in range(100):
    if times[i] > times[most]:
        most = i
print(f"100 functions, 500 logs: function {most} longest, {times[most]} units")
