/*
 * Benchmark workload — Edit Distance (LeetCode #72).
 * C mirror of bench/edit_distance.kara. Faithful to the kata's Vec-based DP: each
 * DP row and input string is a growable buffer built by `push` (realloc doubling),
 * matching Kāra's `Vec.new()+push` growth — NOT a fixed stack array — so the
 * comparison measures the same growing-dynamic-array discipline. Rolling
 * O(n)-space Levenshtein, K=400_000 iters over length-24 pairs.
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

/* Minimal growable i64 vector: new/push mirror Kāra's Vec.new()/push. */
typedef struct { int64_t *data; int64_t len, cap; } Vec;
static Vec vec_new(void) { Vec v = {NULL, 0, 0}; return v; }
static void vpush(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 1;
        v->data = (int64_t *)realloc(v->data, sizeof(int64_t) * (size_t)v->cap);
    }
    v->data[v->len++] = x;
}
static void vfree(Vec *v) { free(v->data); }

typedef struct { unsigned char *data; int64_t len, cap; } Bytes;
static Bytes b_new(void) { Bytes v = {NULL, 0, 0}; return v; }
static void bpush(Bytes *v, unsigned char x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 1;
        v->data = (unsigned char *)realloc(v->data, (size_t)v->cap);
    }
    v->data[v->len++] = x;
}
static void bfree(Bytes *v) { free(v->data); }

static int64_t edit_distance(const unsigned char *a, const unsigned char *b, int64_t m, int64_t n) {
    Vec prev = vec_new();
    for (int64_t j = 0; j <= n; j++) vpush(&prev, j);
    for (int64_t i = 1; i <= m; i++) {
        Vec cur = vec_new();
        vpush(&cur, i);
        for (int64_t j = 1; j <= n; j++) {
            if (a[i - 1] == b[j - 1]) {
                vpush(&cur, prev.data[j - 1]);
            } else {
                int64_t x = prev.data[j - 1];
                if (prev.data[j] < x) x = prev.data[j];
                if (cur.data[j - 1] < x) x = cur.data[j - 1];
                vpush(&cur, 1 + x);
            }
        }
        vfree(&prev);
        prev = cur;
    }
    int64_t r = prev.data[n];
    vfree(&prev);
    return r;
}

int main(void) {
    const int64_t total = 400000, modulus = 1000000007;
    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        Bytes a = b_new(), b = b_new();
        for (int64_t p = 0; p < 24; p++) {
            bpush(&a, (unsigned char)((p * 7 + k) % 4));
            bpush(&b, (unsigned char)((p * 5 + 2 * k) % 4));
        }
        int64_t d = edit_distance(a.data, b.data, 24, 24);
        acc = (acc * 131 + d) % modulus;
        bfree(&a);
        bfree(&b);
    }
    printf("%lld\n", (long long)acc);
    return 0;
}
