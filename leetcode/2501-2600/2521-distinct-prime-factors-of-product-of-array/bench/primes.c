// LeetCode #2521: Distinct Prime Factors of Product of Array -- C mirror of
// the benchmark (primes.kara): the same lists, passes, order and checksum.
// The Set is a small open-addressing hash set, cleared for every call.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define SLOTS 2048
static int64_t table[SLOTS];
static int64_t size;

static void insert(int64_t key) {
    uint64_t h = ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 53;
    while (table[h] != 0) {
        if (table[h] == key) return;
        h = (h + 1) & (SLOTS - 1);
    }
    table[h] = key;
    size++;
}

static int64_t distinct_prime_factors(const int64_t *nums, int64_t n) {
    memset(table, 0, sizeof table);
    size = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t rest = nums[i];
        for (int64_t d = 2; d * d <= rest; d++) {
            if (rest % d == 0) {
                insert(d);
                while (rest % d == 0) rest /= d;
            }
        }
        if (rest > 1) insert(rest);
    }
    return size;
}

static int64_t seed = 2521;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t lists[200][1000];

int main(void) {
    for (int t = 0; t < 200; t++)
        for (int i = 0; i < 1000; i++) lists[t][i] = next_random() % 999 + 2;
    const int passes = 110;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        for (int t = 0; t < 200; t++) {
            int64_t n = check % 1000 + 1;
            check = (check * 31 + distinct_prime_factors(lists[t], n) + p) % 1000000007;
        }
    }
    printf("%d passes over 200 lists of 1000 numbers: checksum %lld\n", passes, (long long)check);
    return 0;
}
