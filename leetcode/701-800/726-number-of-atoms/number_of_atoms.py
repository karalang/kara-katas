# LeetCode #726: Number of Atoms — known-correct reference (dual oracle).
#
# Recursive-descent parse with a stack of count maps; the external answer the
# .kara backends are checked against (interp == codegen agreement alone cannot
# catch a bug both backends share — phase-12 § Bug triage, case (b)).

from collections import defaultdict


def number_of_atoms(formula: str) -> str:
    i, n = 0, len(formula)

    def parse():
        nonlocal i
        counts = defaultdict(int)
        while i < n and formula[i] != ')':
            if formula[i] == '(':
                i += 1
                inner = parse()
                i += 1  # skip ')'
                mult = read_num()
                for name, c in inner.items():
                    counts[name] += c * mult
            else:
                name = formula[i]
                i += 1
                while i < n and formula[i].islower():
                    name += formula[i]
                    i += 1
                counts[name] += read_num()
        return counts

    def read_num():
        nonlocal i
        start = i
        while i < n and formula[i].isdigit():
            i += 1
        return int(formula[start:i]) if i > start else 1

    counts = parse()
    out = []
    for name in sorted(counts):
        out.append(name)
        if counts[name] > 1:
            out.append(str(counts[name]))
    return "".join(out)


CASES = [
    "H2O", "Mg(OH)2", "K4(ON(SO3)2)2",
    "H", "O2", "HOH",
    "Mg", "MgO", "NaCl", "CaCO3",
    "(NB3)33", "(N(B3)2)2", "K4(ON(SO3)2)2", "A2B(C3)2",
    "((H)2O)2", "Be32", "(Be32)1",
]

if __name__ == "__main__":
    for s in CASES:
        print(f'"{s}" -> "{number_of_atoms(s)}"')
