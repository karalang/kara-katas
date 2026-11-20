# LeetCode #1736: Latest Time by Replacing Hidden Digits -- mirrors time.kara
# (the ★ arm).


def maximum_time(time):
    t = list(time)
    if t[0] == "?":
        t[0] = "2" if t[1] == "?" or t[1] <= "3" else "1"
    if t[1] == "?":
        t[1] = "3" if t[0] == "2" else "9"
    if t[3] == "?":
        t[3] = "5"
    if t[4] == "?":
        t[4] = "9"
    return "".join(t)


seed = 1736


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, hide):
    minutes = 0
    check = 0
    for _ in range(count):
        t = next_random() % 1440
        shown = f"{t // 60 // 10}{t // 60 % 10}:{t % 60 // 10}{t % 60 % 10}"
        hidden = ""
        for c in shown:
            if c != ":" and next_random() % hide == 0:
                hidden += "?"
            else:
                hidden += c
        answer = maximum_time(hidden)
        h, m = answer.split(":")
        minutes += int(h) * 60 + int(m)
        for c in answer:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"{count} times with 1 digit in {hide} hidden: latest times sum to {minutes} minutes, checksum {check}")


print(maximum_time("2?:?0"))
print(maximum_time("0?:3?"))
print(maximum_time("1?:22"))
print(maximum_time("??:??"))
print(maximum_time("13:07"))
print(maximum_time("2?:5?"))
print(maximum_time("?4:??"))
batch(3000, 2)
batch(3000, 4)
batch(3000, 1)
