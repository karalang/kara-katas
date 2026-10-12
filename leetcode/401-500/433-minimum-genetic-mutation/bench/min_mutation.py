# Benchmark for #433: mirror of min_mutation.kara (breadth first,
# generating neighbours).
import sys


def min_mutation(start_gene, end_gene, bank):
    unreached = set(bank)
    if end_gene not in unreached:
        return -1
    unreached.discard(start_gene)
    level = [start_gene]
    steps = 0
    while level:
        nxt = []
        for gene in level:
            if gene == end_gene:
                return steps
            for i in range(len(gene)):
                for c in "ACGT":
                    if c != gene[i]:
                        mutant = gene[:i] + c + gene[i + 1:]
                        if mutant in unreached:
                            unreached.remove(mutant)
                            nxt.append(mutant)
        level = nxt
        steps += 1
    return -1


seed = 433


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mutate(gene):
    at = next_random() % 8
    shift = 1 + next_random() % 3
    out = []
    for i, c in enumerate(gene):
        out.append("ACGT"[("ACGT".index(c) + shift) % 4] if i == at else c)
    return "".join(out)


def main():
    size = 1000
    searches = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    bank = ["ACGTACGT"]
    while len(bank) < size:
        parent = bank[next_random() % len(bank)]
        bank.append(mutate(parent))
    reachable = 0
    checksum = 0
    for _ in range(searches):
        start = mutate(bank[next_random() % size])
        end = bank[next_random() % size]
        answer = min_mutation(start, end, bank)
        if answer >= 0:
            reachable += 1
        checksum = (checksum * 31 + answer + 2) % 1000000007
    print(f"{searches} searches in a bank of {size}: {reachable} reachable, checksum {checksum}")


main()
