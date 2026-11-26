# LeetCode #1409 bench, Python: the same P, each query found and the part
# up to it turned one place, workload and checksum as process_queries.kara.


def process_queries(queries, m):
    p = list(range(1, m + 1))
    answer = []
    for q in queries:
        at = p.index(q)
        answer.append(at)
        p[:at + 1] = [q] + p[:at]
    return answer


def main():
    seed = 1409
    check = 0
    for _ in range(300):
        queries = []
        for _ in range(1000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            queries.append(1 + seed // 65536 % 1000)
        for x in process_queries(queries, 1000):
            check = (check * 131 + x) % 1000000007
    print(f"300 rounds of 10^3 queries: checksum {check}")


main()
