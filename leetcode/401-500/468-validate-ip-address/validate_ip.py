# LeetCode #468: Validate IP Address -- split on the separator.
# Mirror of validate_ip.kara (the ★ arm), with the same harness.


def ipv4_part(part):
    if len(part) == 0 or len(part) > 3:
        return False
    value = 0
    for c in part:
        if not ("0" <= c <= "9"):
            return False
        value = value * 10 + (ord(c) - 48)
    if len(part) > 1 and part.startswith("0"):
        return False
    return value <= 255


def ipv6_group(group):
    if len(group) == 0 or len(group) > 4:
        return False
    for c in group:
        if c not in "0123456789abcdefABCDEF":
            return False
    return True


def valid_ip_address(query_ip):
    if "." in query_ip:
        parts = 0
        for part in query_ip.split("."):
            if not ipv4_part(part):
                return "Neither"
            parts += 1
        if parts == 4:
            return "IPv4"
    elif ":" in query_ip:
        groups = 0
        for group in query_ip.split(":"):
            if not ipv6_group(group):
                return "Neither"
            groups += 1
        if groups == 8:
            return "IPv6"
    return "Neither"


# ---- test harness ----------------------------------------------------------


def show(query_ip):
    answer = valid_ip_address(query_ip)
    print(f'"{query_ip}" -> {answer}')


seed = 468


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def pick(alphabet):
    return alphabet[next_random() % len(alphabet)]


def random_query():
    kind = next_random() % 5
    fault = next_random() % 8
    s = []
    if kind < 2:
        parts = [3, 5][next_random() % 2] if fault == 4 else 4
        at = next_random() % parts
        for p in range(parts):
            if p > 0:
                s.append(".")
            value = next_random() % 256
            if p == at and fault == 5:
                s.append("0")
            if p == at and fault == 6:
                value = 256 + next_random() % 744
            if p == at and fault == 7:
                if next_random() % 2 == 0:
                    s.append(pick("aeFx"))
                continue
            s.append(f"{value}")
    elif kind < 4:
        groups = [7, 9][next_random() % 2] if fault == 4 else 8
        at = next_random() % groups
        for g in range(groups):
            if g > 0:
                s.append(":")
            if g == at and fault == 6:
                continue
            length = 5 if g == at and fault == 5 else 1 + next_random() % 4
            bad = next_random() % length if g == at and fault == 7 else -1
            for i in range(length):
                if i == bad:
                    s.append(pick("gGxz"))
                else:
                    s.append(pick("0123456789abcdefABCDEF"))
    else:
        length = 1 + next_random() % 15
        for _ in range(length):
            s.append(pick("0123456789aF.:g"))
    return "".join(s)


def main():
    for q in ["172.16.254.1", "2001:0db8:85a3:0:0:8A2E:0370:7334", "256.256.256.256",
              "0.0.0.0", "255.255.255.255", "01.1.1.1", "00.0.0.0", "1.1.1", "1.1.1.1.",
              ".1.1.1", "1..1.1", "1e1.4.5.6", "192.168.1.1:80", "1:2:3:4:5:6:7:8",
              "abcd:ABCD:Ef01:9:0:0:0:0", "2001:db8:85a3:0::8a2E:0370:7334",
              "02001:0db8:85a3:0000:0000:8a2e:0370:7334",
              "2001:0db8:85a3:0:0:8A2E:0370:7334:", "G:1:2:3:4:5:6:7",
              "1.2.3.4.5.6.7.8", "a"]:
        show(q)
    count = 300
    ipv4 = ipv6 = neither = 0
    checksum = 0
    for _ in range(count):
        answer = valid_ip_address(random_query())
        if answer == "IPv4":
            ipv4 += 1
            code = 1
        elif answer == "IPv6":
            ipv6 += 1
            code = 2
        else:
            neither += 1
            code = 3
        checksum = (checksum * 7 + code) % 1000000007
    print(f"{count} random queries: {ipv4} IPv4, {ipv6} IPv6, {neither} Neither, checksum {checksum}")


main()
