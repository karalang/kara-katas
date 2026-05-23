/*
 * LeetCode 1 — hash-map O(n) Two Sum, bench mirror in C.
 *
 * Algorithmic mirror of bench/hash_map.kara and bench/hash_map.rs. Same
 * N=5000, K=10, sentinel target=-1 (never matches; full pass per call).
 * Stdout sink: K * (-1 + -1) = -20.
 *
 * C has no hashmap in libc, so this carries a small open-addressing,
 * linear-probing hashmap keyed by i64 with i64 values. Capacity is a
 * power of two >= 2*N for ~0.5 load factor (matches the working point
 * Rust's HashMap and kara's Map[K, V] sit at). No deletes — `two_sum`
 * builds fresh per call.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define N 5000
#define CAP 16384   /* power of two, >= 2 * N */

static int64_t keys[CAP];
static size_t  vals[CAP];
static bool    used[CAP];

static inline size_t hash_key(int64_t k) {
    /* splitmix-ish: cheap, decent dispersion for the small integer keys. */
    uint64_t x = (uint64_t)k;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
    x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
    x =  x ^ (x >> 31);
    return (size_t)(x & (CAP - 1));
}

static void map_reset(void) {
    memset(used, 0, sizeof used);
}

static bool map_get(int64_t k, size_t *out) {
    size_t h = hash_key(k);
    for (;;) {
        if (!used[h]) return false;
        if (keys[h] == k) { *out = vals[h]; return true; }
        h = (h + 1) & (CAP - 1);
    }
}

static void map_insert(int64_t k, size_t v) {
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

static int two_sum(const int64_t *nums, int64_t target, size_t *oi, size_t *oj) {
    map_reset();
    for (size_t i = 0; i < N; i++) {
        int64_t complement = target - nums[i];
        size_t j;
        if (map_get(complement, &j)) {
            *oi = j;
            *oj = i;
            return 1;
        }
        map_insert(nums[i], i);
    }
    return 0;
}

int main(void) {
    int64_t data[N];
    for (size_t i = 0; i < N; i++) {
        data[i] = ((int64_t)i * 7) % 1000;
    }

    const int64_t target = -1;
    int64_t sum = 0;
    for (int k = 0; k < 10; k++) {
        size_t i, j;
        if (two_sum(data, target, &i, &j)) {
            sum += (int64_t)i + (int64_t)j;
        } else {
            sum += -2;
        }
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
