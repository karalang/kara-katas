# Benchmark for #468: mirror of validate_ip.kara (the ★ arm: split on the
# separator) on the same workload.


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
    count = 100000
    rounds = 20
    queries = [random_query() for _ in range(count)]
    ipv4 = ipv6 = 0
    checksum = 0
    for _ in range(rounds):
        for i in range(count):
            answer = valid_ip_address(queries[i])
            if answer == "IPv4":
                ipv4 += 1
                code = 1
            elif answer == "IPv6":
                ipv6 += 1
                code = 2
            else:
                code = 3
            checksum = (checksum * 7 + code + i) % 1000000007
    print(f"{rounds} rounds of {count} queries: {ipv4} IPv4, {ipv6} IPv6, checksum {checksum}")


main()
