# LeetCode #433: Minimum Genetic Mutation -- mirror of min_mutation.kara
# (breadth first, generating neighbours).


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


def show(start_gene, end_gene, bank):
    print(f"{start_gene} -> {end_gene}, bank of {len(bank)}: {min_mutation(start_gene, end_gene, bank)}")


def bank_of(genes):
    return genes.split(" ") if genes else []


seed = 433


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_gene():
    return "".join("ACGT"[next_random() % 4] for _ in range(8))


def mutate(gene):
    at = next_random() % 8
    shift = 1 + next_random() % 3
    out = []
    for i, c in enumerate(gene):
        out.append("ACGT"[("ACGT".index(c) + shift) % 4] if i == at else c)
    return "".join(out)


def main():
    show("AACCGGTT", "AACCGGTA", bank_of("AACCGGTA"))
    show("AACCGGTT", "AAACGGTA", bank_of("AACCGGTA AACCGCTA AAACGGTA"))
    show("AAAAACCC", "AACCCCCC", bank_of("AAAACCCC AAACCCCC AACCCCCC"))
    show("AACCGGTT", "AACCGGTA", bank_of(""))
    show("AACCGGTT", "AACCGGTA", bank_of("AACCGGTC AACCGGAA"))
    show("AAAAAAAA", "CCCCCCCC", bank_of("AAAAAAAC AAAAAACC AAAAACCC AAAACCCC AAACCCCC AACCCCCC ACCCCCCC CCCCCCCC"))
    show("AAAAAAAA", "AAAAAATT", bank_of("AAAAAAAT AAAAAATT AAAAAAAA"))
    show("AAAAAAAA", "TTTTTTTT", bank_of("TTTTTTTT AAAAAAAT"))
    reachable = 0
    total = 0
    checksum = 0
    for _ in range(300):
        start = random_gene()
        size = next_random() % 31
        bank = []
        last = start
        for _ in range(size):
            if next_random() % 5 == 0:
                last = random_gene()
            else:
                last = mutate(last)
            bank.append(last)
        if size > 0 and next_random() % 4 != 0:
            end = bank[next_random() % size]
        else:
            end = random_gene()
        answer = min_mutation(start, end, bank)
        if answer >= 0:
            reachable += 1
            total += answer
        checksum = (checksum * 31 + answer + 2) % 1000000007
    print(f"300 random banks: {reachable} reachable, {total} mutations in all, checksum {checksum}")


main()
