// Benchmark workload for LeetCode #248 — Strobogrammatic Number III (C mirror).
// Mirrors strobogrammatic_count.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char **s; long len; long cap; } Vec;
static void vpush(Vec *v, char *x) {
    if (v->len == v->cap) { v->cap = v->cap ? v->cap * 2 : 16; v->s = realloc(v->s, v->cap * sizeof(char *)); }
    v->s[v->len++] = x;
}
static void vfree(Vec *v) { for (long i = 0; i < v->len; i++) free(v->s[i]); free(v->s); }

static const char PA[5] = {'0','1','6','8','9'};
static const char PB[5] = {'0','1','9','8','6'};

static long pow5(long e) { long a = 1; for (long i = 0; i < e; i++) a *= 5; return a; }

static long count_of_length(long len) {
    if (len <= 0) return 0;
    if (len == 1) return 3;
    long t = 4 * pow5(len / 2 - 1);
    if (len % 2 == 1) t *= 3;
    return t;
}

static Vec build(long k, long n) {
    Vec out = {0,0,0};
    if (k == 0) { vpush(&out, strdup("")); return out; }
    if (k == 1) { vpush(&out, strdup("0")); vpush(&out, strdup("1")); vpush(&out, strdup("8")); return out; }
    Vec inner = build(k - 2, n);
    for (long i = 0; i < inner.len; i++) {
        for (int p = 0; p < 5; p++) {
            if (PA[p] == '0' && k == n) continue;
            long il = (long)strlen(inner.s[i]);
            char *s = malloc(il + 3);
            s[0] = PA[p]; memcpy(s + 1, inner.s[i], il); s[1+il] = PB[p]; s[2+il] = '\0';
            vpush(&out, s);
        }
    }
    vfree(&inner);
    return out;
}

static long cmp_digits(const char *a, const char *b) {
    long la = (long)strlen(a), lb = (long)strlen(b);
    if (la != lb) return la < lb ? -1 : 1;
    for (long i = 0; i < la; i++)
        if (a[i] != b[i]) return (unsigned char)a[i] < (unsigned char)b[i] ? -1 : 1;
    return 0;
}

static long count_bounded(long len, const char *low, const char *high, int use_lo, int use_hi) {
    Vec c = build(len, len);
    long n = 0;
    for (long i = 0; i < c.len; i++) {
        int keep = 1;
        if (use_lo && cmp_digits(c.s[i], low) < 0) keep = 0;
        if (use_hi && cmp_digits(c.s[i], high) > 0) keep = 0;
        if (keep) n++;
    }
    vfree(&c);
    return n;
}

static long count_in_range(const char *low, const char *high) {
    long ll = (long)strlen(low), hl = (long)strlen(high);
    if (ll > hl) return 0;
    if (ll == hl) {
        if (cmp_digits(low, high) > 0) return 0;
        return count_bounded(ll, low, high, 1, 1);
    }
    long total = count_bounded(ll, low, high, 1, 0);
    total += count_bounded(hl, low, high, 0, 1);
    for (long len = ll + 1; len < hl; len++) total += count_of_length(len);
    return total;
}

static void digits_of(long v, char *buf) {
    if (v == 0) { buf[0] = '0'; buf[1] = '\0'; return; }
    char tmp[32]; int n = 0;
    while (v > 0) { tmp[n++] = (char)('0' + v % 10); v /= 10; }
    for (int i = 0; i < n; i++) buf[i] = tmp[n - 1 - i];
    buf[n] = '\0';
}

int main(void) {
    long queries = 1000, state = 248248, sink = 0;
    char ba[32], bb[32];
    for (long q = 0; q < queries; q++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long da = (state / 65536L) % 8L + 1L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long db = (state / 65536L) % 8L + 1L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long ra = (state / 65536L) % 9000L + 1L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long rb = (state / 65536L) % 9000L + 1L;

        long a = ra;
        for (long i = 1; i < da; i++) a = a * 10 % 1000000000000000L + (i % 10);
        long b = rb;
        for (long j = 1; j < db; j++) b = b * 10 % 1000000000000000L + (j % 10);
        if (a > b) { long t = a; a = b; b = t; }

        digits_of(a, ba); digits_of(b, bb);
        sink = (sink + count_in_range(ba, bb)) % 1000000007L;
    }
    printf("%ld\n", sink);
    return 0;
}
