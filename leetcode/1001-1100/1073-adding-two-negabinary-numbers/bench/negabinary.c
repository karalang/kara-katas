// LeetCode #1073: Adding Two Negabinary Numbers -- the benchmark's C mirror
// of negabinary.kara: the same addition from the low end with a carry, the
// digits pushed onto a growing array, over 2000 pairs of numbers built
// once, each added 20 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *d;
    int64_t n, cap;
} digits;

static void push(digits *v, int64_t x) {
    if (v->n == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->d = realloc(v->d, v->cap * sizeof(int64_t));
    }
    v->d[v->n++] = x;
}

static digits add_negabinary(const digits *a, const digits *b) {
    int64_t i = a->n - 1, j = b->n - 1, carry = 0;
    digits out = {0, 0, 0};
    while (i >= 0 || j >= 0 || carry != 0) {
        int64_t s = carry;
        if (i >= 0) s += a->d[i--];
        if (j >= 0) s += b->d[j--];
        push(&out, s & 1);
        carry = -(s >> 1);
    }
    while (out.n > 1 && out.d[out.n - 1] == 0) out.n--;
    for (int64_t l = 0, r = out.n - 1; l < r; l++, r--) {
        int64_t t = out.d[l];
        out.d[l] = out.d[r];
        out.d[r] = t;
    }
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static digits random_number(int64_t longest, int64_t *seed) {
    digits v = {0, 0, 0};
    int64_t n = next_random(seed) % longest + 1;
    if (n == 1) {
        push(&v, next_random(seed) % 2);
        return v;
    }
    push(&v, 1);
    for (int64_t k = 1; k < n; k++) push(&v, next_random(seed) % 2);
    return v;
}

int main(void) {
    int64_t seed = 1073;
    static digits as[2000], bs[2000];
    for (int k = 0; k < 2000; k++) {
        as[k] = random_number(1000, &seed);
        bs[k] = random_number(1000, &seed);
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 20; r++) {
        for (int k = 0; k < 2000; k++) {
            digits x = add_negabinary(&as[k], &bs[k]);
            total += x.n;
            check = (check * 31 + x.n + x.d[x.n / 2]) % 1000000007;
            free(x.d);
        }
    }
    printf("40000 calls: %lld digits, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
