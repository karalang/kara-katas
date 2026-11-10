// LeetCode #1106: Parsing A Boolean Expression -- the bench in C: the ★
// arm (recursive descent from a shared position) over 32 expressions of
// up to about 2 * 10^4 characters, each round flipping one value in every
// expression and parsing it again. Characters are 32-bit, as Kāra's
// `char` and Rust's are, and each operator's values a growable array.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

static bool parse(const int32_t *s, int64_t *at) {
    int32_t c = s[*at];
    *at += 1;
    if (c == 't') return true;
    if (c == 'f') return false;
    *at += 1;
    int64_t len = 0, cap = 4;
    bool *values = malloc((size_t)cap * sizeof(bool));
    for (;;) {
        bool v = parse(s, at);
        if (len == cap) {
            cap *= 2;
            values = realloc(values, (size_t)cap * sizeof(bool));
        }
        values[len++] = v;
        int32_t next = s[*at];
        *at += 1;
        if (next == ')') break;
    }
    bool r;
    if (c == '!') {
        r = !values[0];
    } else if (c == '&') {
        r = true;
        for (int64_t i = 0; i < len; i++) if (!values[i]) { r = false; break; }
    } else {
        r = false;
        for (int64_t i = 0; i < len; i++) if (values[i]) { r = true; break; }
    }
    free(values);
    return r;
}

static int64_t seed = 1106;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct { int32_t *data; int64_t len, cap; } Buf;
static void put(Buf *b, int32_t c) {
    if (b->len == b->cap) {
        b->cap = b->cap ? b->cap * 2 : 16;
        b->data = realloc(b->data, (size_t)b->cap * sizeof(int32_t));
    }
    b->data[b->len++] = c;
}

static void random_expr(Buf *out, int64_t budget, int64_t depth) {
    if (budget <= 1 || depth == 0) {
        put(out, next_random() % 2 == 0 ? 't' : 'f');
        return;
    }
    int64_t op = next_random() % 3;
    if (op == 0) {
        put(out, '!');
        put(out, '(');
        random_expr(out, budget - 1, depth - 1);
        put(out, ')');
        return;
    }
    int64_t k = next_random() % 4 + 1;
    put(out, op == 1 ? '&' : '|');
    put(out, '(');
    for (int64_t i = 0; i < k; i++) {
        if (i > 0) put(out, ',');
        random_expr(out, (budget - 1) / k, depth - 1);
    }
    put(out, ')');
}

int main(void) {
    Buf cases[32] = {0};
    int64_t *values[32];
    int64_t nvalues[32];
    int64_t length = 0;
    for (int c = 0; c < 32; c++) {
        random_expr(&cases[c], 6000, 20);
        values[c] = malloc((size_t)cases[c].len * sizeof(int64_t));
        nvalues[c] = 0;
        for (int64_t i = 0; i < cases[c].len; i++)
            if (cases[c].data[i] == 't' || cases[c].data[i] == 'f') values[c][nvalues[c]++] = i;
        length += cases[c].len;
    }
    int64_t trues = 0, check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int64_t j = 0; j < 32; j++) {
            int64_t i = values[j][(round * 7919 + j * 104729) % nvalues[j]];
            cases[j].data[i] = cases[j].data[i] == 't' ? 'f' : 't';
            int64_t at = 0;
            bool v = parse(cases[j].data, &at);
            if (v) trues++;
            check = (check * 31 + (v ? 2 : 1)) % 1000000007;
        }
    }
    printf("200 rounds over 32 expressions of %lld characters: %lld true, checksum %lld\n", (long long)length, (long long)trues, (long long)check);
    return 0;
}
