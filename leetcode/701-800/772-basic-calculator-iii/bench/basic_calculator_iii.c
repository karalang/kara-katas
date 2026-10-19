// LeetCode 772 — Basic Calculator III: benchmark, the ★ arm in C.
// Sixty-four random expressions of 2,400 numbers, up to LeetCode's limit
// of 10,000 characters, built once; ROUNDS rounds each evaluate the next.
// At each operator the generator takes the first, from a random start,
// that keeps every value valid: no division by zero, nothing beyond 32
// bits.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define ROUNDS 6000
#define LEAVES 2400

typedef struct {
    const char *s;
    size_t n, at;
} Cursor;

static int64_t sum(Cursor *c);

static char peek(const Cursor *c) { return c->at < c->n ? c->s[c->at] : 0; }

static int64_t factor(Cursor *c) {
    if (peek(c) == '(') {
        c->at += 1;
        int64_t value = sum(c);
        c->at += 1;
        return value;
    }
    int64_t value = 0;
    while (peek(c) >= '0' && peek(c) <= '9') {
        value = value * 10 + (peek(c) - '0');
        c->at += 1;
    }
    return value;
}

static int64_t term(Cursor *c) {
    int64_t value = factor(c);
    for (;;) {
        char op = peek(c);
        if (op != '*' && op != '/') return value;
        c->at += 1;
        int64_t right = factor(c);
        value = op == '*' ? value * right : value / right;
    }
}

static int64_t sum(Cursor *c) {
    int64_t value = term(c);
    for (;;) {
        char op = peek(c);
        if (op != '+' && op != '-') return value;
        c->at += 1;
        int64_t right = term(c);
        value = op == '+' ? value + right : value - right;
    }
}

static int64_t calculate(const char *s, size_t n) {
    Cursor c = {s, n, 0};
    return sum(&c);
}

static int64_t seed = 772;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// Writes a op b to *out; 0 if b is 0 under / or the value leaves 32 bits.
static int combine(int64_t a, char op, int64_t b, int64_t *out) {
    if (op == '/' && b == 0) return 0;
    int64_t v = op == '+' ? a + b : op == '-' ? a - b : op == '*' ? a * b : a / b;
    if (v < -2147483648LL || v > 2147483647LL) return 0;
    *out = v;
    return 1;
}

typedef struct {
    char *text;
    size_t len;
    int64_t value;
    int level;
} Piece;

static Piece build(int64_t leaves) {
    Piece p;
    if (leaves == 1) {
        int64_t n = next_random() % 4 == 0 ? next_random() % 1000 : next_random() % 10;
        p.text = malloc(8);
        p.len = (size_t)sprintf(p.text, "%lld", (long long)n);
        p.value = n;
        p.level = 3;
        return p;
    }
    int64_t left_leaves = 1 + next_random() % (leaves - 1);
    Piece left = build(left_leaves);
    Piece right = build(leaves - left_leaves);
    const char *ops = "+-*/";
    int64_t k = next_random() % 4, value;
    while (!combine(left.value, ops[k], right.value, &value)) k = (k + 1) % 4;
    char op = ops[k];
    int level = op == '+' || op == '-' ? 1 : 2;
    int lb = left.level < level || next_random() % 4 == 0;
    int rb = right.level < level || (right.level == level && op != '+') || next_random() % 4 == 0;
    p.text = malloc(left.len + right.len + 6);
    size_t at = 0;
    if (lb) p.text[at++] = '(';
    memcpy(p.text + at, left.text, left.len);
    at += left.len;
    if (lb) p.text[at++] = ')';
    p.text[at++] = op;
    if (rb) p.text[at++] = '(';
    memcpy(p.text + at, right.text, right.len);
    at += right.len;
    if (rb) p.text[at++] = ')';
    p.text[at] = 0;
    p.len = at;
    p.value = value;
    p.level = level;
    free(left.text);
    free(right.text);
    return p;
}

int main(void) {
    Piece pool[64];
    size_t longest = 0;
    for (int i = 0; i < 64; i++) {
        pool[i] = build(LEAVES);
        if (pool[i].len > longest) longest = pool[i].len;
    }
    int64_t check = 0;
    for (int64_t round = 0; round < ROUNDS; round++) {
        int64_t value = calculate(pool[round % 64].text, pool[round % 64].len);
        check = ((check * 31 + value) % 1000000007 + 1000000007) % 1000000007;
    }
    printf("%d expressions of up to %zu characters: checksum %lld\n", ROUNDS, longest, (long long)check);
    return 0;
}
