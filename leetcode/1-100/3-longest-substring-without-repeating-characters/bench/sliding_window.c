/*
 * LeetCode 3 — sliding-window O(n) Longest Substring Without Repeating
 * Characters, bench mirror in C.
 *
 * Algorithmic mirror of bench/sliding_window.{kara,rs,py}. Same input:
 * the 26-character lowercase alphabet repeated 4000 times for a
 * 104_000-char string. K=20 outer iterations. Stdout sink: K * 26 = 520.
 *
 * C has no hashmap in libc, so this carries a small open-addressing,
 * linear-probing hashmap keyed by i32 codepoint with i64 indices —
 * same shape as kata 1's hash_map.c, narrowed to the char alphabet here.
 * Capacity is a power of two >= 2 * sigma (sigma = 26 distinct keys per
 * call); the map is reset per call to match Kāra's `Map.new()` per
 * `length_of_longest_substring` invocation.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

#define CAP 64   /* power of two, >= 2 * sigma where sigma <= 26 here */

static int32_t keys[CAP];
static int64_t vals[CAP];
static bool    used[CAP];

static inline size_t hash_key(int32_t k) {
    /* splitmix-ish: cheap, decent dispersion for small integer keys. */
    uint64_t x = (uint64_t)(uint32_t)k;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    x =  x ^ (x >> 31);
    return (size_t)(x & (CAP - 1));
}

static void map_reset(void) {
    memset(used, 0, sizeof used);
}

static bool map_get(int32_t k, int64_t *out) {
    size_t h = hash_key(k);
    for (;;) {
        if (!used[h]) return false;
        if (keys[h] == k) { *out = vals[h]; return true; }
        h = (h + 1) & (CAP - 1);
    }
}

static void map_insert(int32_t k, int64_t v) {
    size_t h = hash_key(k);
    for (;;) {
        if (!used[h]) {
            used[h] = true;
            keys[h] = k;
            vals[h] = v;
            return;
        }
        if (keys[h] == k) { vals[h] = v; return; }
        h = (h + 1) & (CAP - 1);
    }
}

static int64_t length_of_longest_substring(const char *s, size_t n) {
    map_reset();
    int64_t left = 0;
    int64_t best = 0;
    for (size_t right = 0; right < n; right++) {
        int32_t c = (int32_t)(unsigned char)s[right];
        int64_t prev;
        if (map_get(c, &prev) && prev >= left) {
            left = prev + 1;
        }
        map_insert(c, (int64_t)right);
        int64_t window = (int64_t)right - left + 1;
        if (window > best) best = window;
    }
    return best;
}

int main(void) {
    const size_t N = 104000;   /* 26 * 4000 */
    char *data = (char *)malloc(N + 1);
    const char *alpha = "abcdefghijklmnopqrstuvwxyz";
    for (size_t i = 0; i < N; i++) data[i] = alpha[i % 26];
    data[N] = '\0';

    int64_t sum = 0;
    for (int k = 0; k < 20; k++) {
        sum += length_of_longest_substring(data, N);
    }
    printf("%lld\n", (long long)sum);
    free(data);
    return 0;
}
