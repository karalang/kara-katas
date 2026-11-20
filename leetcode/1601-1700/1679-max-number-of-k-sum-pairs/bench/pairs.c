// LeetCode #1679: Max Number of K-Sum Pairs -- the bench's C mirror: the ★
// arm on 50 arrays of 100000 values up to 100000, each with a k up to
// 200000, all drawn first, each answered 10 times. C has no hash map; an
// open-addressing one written for the bench, cleared for each answer.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ARRAYS 50
#define N 100000
#define MOST 100000
#define ROUNDS 10
#define SLOTS (1 << 18)

static int32_t keys[SLOTS];
static int32_t counts[SLOTS];
static uint8_t used[SLOTS];

static uint32_t slot_of(int32_t key) {
    uint32_t i = ((uint32_t)key * 2654435761u) >> 14;
    while (used[i] && keys[i] != key) i = (i + 1) & (SLOTS - 1);
    return i;
}

static int32_t max_operations(const int32_t *nums, int64_t n, int32_t k) {
    memset(used, 0, sizeof used);
    int32_t operations = 0;
    for (int64_t i = 0; i < n; i++) {
        int32_t x = nums[i];
        uint32_t p = slot_of(k - x);
        if (used[p] && counts[p] > 0) {
            counts[p] -= 1;
            operations += 1;
        } else {
            uint32_t s = slot_of(x);
            if (!used[s]) {
                used[s] = 1;
                keys[s] = x;
                counts[s] = 0;
            }
            counts[s] += 1;
        }
    }
    return operations;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1679;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t nums[ARRAYS][N];
    static int32_t ks[ARRAYS];
    for (int a = 0; a < ARRAYS; a++) {
        for (int i = 0; i < N; i++) nums[a][i] = (int32_t)((next_random() * 32768 + next_random()) % MOST + 1);
        ks[a] = (int32_t)((next_random() * 32768 + next_random()) % (2 * MOST - 1) + 2);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < ARRAYS; a++) {
            int64_t operations = max_operations(nums[a], N, ks[a]);
            total += operations;
            check = (check * 31 + operations + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: %lld operations, checksum %lld\n", ARRAYS, N, ROUNDS, (long long)total, (long long)check);
    return 0;
}
