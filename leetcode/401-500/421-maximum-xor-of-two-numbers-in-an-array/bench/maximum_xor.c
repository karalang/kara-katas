// Benchmark for #421: mirror of maximum_xor.kara (prefix bits). The
// set is open addressing with linear probing and a multiplicative hash,
// sized to a power of two at least twice the count.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t *table;
static uint8_t *used;
static int64_t cap;

static uint64_t slot(int64_t key) {
    return ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 32 & (uint64_t)(cap - 1);
}

static void insert(int64_t key) {
    uint64_t i = slot(key);
    while (used[i]) {
        if (table[i] == key) return;
        i = (i + 1) & (uint64_t)(cap - 1);
    }
    used[i] = 1;
    table[i] = key;
}

static int contains(int64_t key) {
    uint64_t i = slot(key);
    while (used[i]) {
        if (table[i] == key) return 1;
        i = (i + 1) & (uint64_t)(cap - 1);
    }
    return 0;
}

static int64_t find_maximum_xor(const int64_t *nums, int64_t n) {
    cap = 1;
    while (cap < 2 * n) cap *= 2;
    table = malloc(cap * sizeof *table);
    used = malloc(cap);
    int64_t answer = 0, mask = 0;
    for (int64_t bit = 30; bit >= 0; bit--) {
        mask |= (int64_t)1 << bit;
        memset(used, 0, cap);
        for (int64_t i = 0; i < n; i++) insert(nums[i] & mask);
        int64_t candidate = answer | ((int64_t)1 << bit);
        for (int64_t i = 0; i < cap; i++) {
            if (used[i] && contains(table[i] ^ candidate)) {
                answer = candidate;
                break;
            }
        }
    }
    free(table);
    free(used);
    return answer;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random31(int64_t *seed) {
    int64_t high = step(seed);
    int64_t low = step(seed);
    int64_t bit = step(seed) % 2;
    return high * 65536 + low * 2 + bit;
}

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 100;
    int64_t n = 20000, seed = 421;
    int64_t *nums = malloc(n * sizeof *nums);
    for (int64_t i = 0; i < n; i++) nums[i] = random31(&seed);
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        nums[r * 7919 % n] = random31(&seed);
        int64_t answer = find_maximum_xor(nums, n);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld rounds on %lld numbers: total %lld, checksum %lld\n", (long long)rounds, (long long)n, (long long)total, (long long)checksum);
    free(nums);
    return 0;
}
