# LeetCode #636: Exclusive Time of Functions -- benchmark, Python.
#
# The ★ arm: one stack of running functions and the time of the last
# event.


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


def main():
    inputs = [random_logs(100, 250, 3800000) for _ in range(10)]
    total = checksum = 0
    for r in range(10000):
        for t in exclusive_time(100, inputs[r % 10]):
            total += t
            checksum = (checksum * 31 + t) % 1000000007
    print(f"10 inputs of 500 logs, 10000 rounds: total {total}, checksum {checksum}")


main()
