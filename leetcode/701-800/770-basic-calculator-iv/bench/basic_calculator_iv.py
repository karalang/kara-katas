# LeetCode 770 — Basic Calculator IV: benchmark, the ★ arm in Python.
# Sixty-four random expressions of 40 leaves, built once; 20,000 rounds
# each simplify the next of them.


def tokenize(expression):
    tokens = []
    word = ""
    for c in expression:
        if c.isalnum():
            word += c
        else:
            if word:
                tokens.append(word)
                word = ""
            if c != " ":
                tokens.append(c)
    if word:
        tokens.append(word)
    return tokens


def names_of(key):
    return key.split("*") if key else []


def add_into(total, p, sign):
    for key, coef in p.items():
        total[key] = total.get(key, 0) + sign * coef


def multiply(a, b):
    product = {}
    for ka, ca in a.items():
        for kb, cb in b.items():
            key = "*".join(sorted(names_of(ka) + names_of(kb)))
            product[key] = product.get(key, 0) + ca * cb
    return product


class Reader:
    def __init__(self, tokens, known):
        self.tokens = tokens
        self.at = 0
        self.known = known

    def peek(self):
        return self.tokens[self.at] if self.at < len(self.tokens) else ""

    def expression(self):
        total = self.term()
        while self.peek() in ("+", "-"):
            sign = 1 if self.peek() == "+" else -1
            self.at += 1
            add_into(total, self.term(), sign)
        return total

    def term(self):
        product = self.factor()
        while self.peek() == "*":
            self.at += 1
            product = multiply(product, self.factor())
        return product

    def factor(self):
        token = self.peek()
        self.at += 1
        if token == "(":
            p = self.expression()
            self.at += 1
            return p
        if token[0].isdigit():
            return {"": int(token)}
        if token in self.known:
            return {"": self.known[token]}
        return {token: 1}


def basic_calculator_iv(expression, evalvars, evalints):
    poly = Reader(tokenize(expression), dict(zip(evalvars, evalints))).expression()
    terms = sorted((-len(names_of(k)), k, c) for k, c in poly.items() if c != 0)
    return [f"{c}*{k}" if k else f"{c}" for _, k, c in terms]


seed = 770


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_expression(size):
    if size <= 1:
        pick = next_random() % 9
        if pick < 3:
            return f"{next_random() % 10}"
        return ["a", "b", "c", "d", "x", "y"][pick - 3]
    left = 1 + next_random() % (size - 1)
    a = random_expression(left)
    b = random_expression(size - left)
    op = [" + ", " - ", " * "][next_random() % 3]
    if next_random() % 3 == 0:
        return f"({a}{op}{b})"
    return f"{a}{op}{b}"


def main():
    rounds = 20000
    pool = [random_expression(40) for _ in range(64)]
    longest = max(len(e) for e in pool)
    terms = 0
    check = 0
    for rnd in range(rounds):
        answer = basic_calculator_iv(pool[rnd % 64], ["x"], [rnd % 7 - 3])
        terms += len(answer)
        for t in answer:
            for b in t.encode():
                check = (check * 31 + b) % 1000000007
    print(f"{rounds} expressions of up to {longest} characters: {terms} terms in all, checksum {check}")


main()
