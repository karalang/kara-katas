// Benchmark workload for LeetCode #247 — Strobogrammatic Number II (C mirror).
// Mirrors strobogrammatic_ii.kara algorithm-for-algorithm: same middle-outward
// recursion, same outermost 0/0 refusal, same verify-and-checksum read-back.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char **s; long len; long cap; } Vec;

static void vpush(Vec *v, char *x) {
    if (v->len == v->cap) { v->cap = v->cap ? v->cap * 2 : 16; v->s = realloc(v->s, v->cap * sizeof(char *)); }
    v->s[v->len++] = x;
}
static void vfree(Vec *v) { for (long i = 0; i < v->len; i++) free(v->s[i]); free(v->s); }

static const char *PAIR_A[5] = {"0", "1", "6", "8", "9"};
static const char *PAIR_B[5] = {"0", "1", "9", "8", "6"};

static Vec build(long k, long n) {
    Vec out = {0, 0, 0};
    if (k == 0) { vpush(&out, strdup("")); return out; }
    if (k == 1) { vpush(&out, strdup("0")); vpush(&out, strdup("1")); vpush(&out, strdup("8")); return out; }

    Vec inner = build(k - 2, n);
    for (long i = 0; i < inner.len; i++) {
        for (long p = 0; p < 5; p++) {
            if (k == n && PAIR_A[p][0] == '0') continue;
            long ilen = (long)strlen(inner.s[i]);
            char *s = malloc(ilen + 3);
            s[0] = PAIR_A[p][0];
            memcpy(s + 1, inner.s[i], ilen);
            s[1 + ilen] = PAIR_B[p][0];
            s[2 + ilen] = '\0';
            vpush(&out, s);
        }
    }
    vfree(&inner);
    return out;
}

static int is_strobogrammatic(const char *s) {
    long lo = 0, hi = (long)strlen(s) - 1;
    while (lo <= hi) {
        long x = (unsigned char)s[lo], y = (unsigned char)s[hi];
        int ok = (x == 48 && y == 48) || (x == 49 && y == 49) || (x == 56 && y == 56)
              || (x == 54 && y == 57) || (x == 57 && y == 54);
        if (!ok) return 0;
        lo++; hi--;
    }
    return 1;
}

int main(void) {
    long n = 16, rounds = 12, sink = 0;
    for (long r = 0; r < rounds; r++) {
        Vec got = build(n, n);
        for (long i = 0; i < got.len; i++) {
            if (is_strobogrammatic(got.s[i])) {
                for (const unsigned char *p = (const unsigned char *)got.s[i]; *p; p++)
                    sink = (sink * 31 + (long)*p) % 1000000007L;
            }
        }
        vfree(&got);
    }
    printf("%ld\n", sink);
    return 0;
}
