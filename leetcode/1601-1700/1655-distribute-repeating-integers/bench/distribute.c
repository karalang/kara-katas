// LeetCode #1655: Distribute Repeating Integers -- the bench's C mirror:
// the ★ arm on 200 random problems of 100000 numbers from 50 values and
// 10 customers wanting 1 to 3000 each, all drawn first. The counts are
// kept by value in an open-addressing table, as the other languages'
// hash maps keep them.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PROBLEMS 200
#define N 100000
#define M 10
#define SLOTS 256

static bool can_distribute(const int32_t *nums, int n, const int32_t *quantity, int m) {
    int32_t keys[SLOTS];
    int64_t counts[SLOTS];
    bool used[SLOTS] = {false};
    for (int i = 0; i < n; i++) {
        uint32_t h = (uint32_t)nums[i] * 2654435761u % SLOTS;
        while (used[h] && keys[h] != nums[i]) h = (h + 1) % SLOTS;
        if (!used[h]) {
            used[h] = true;
            keys[h] = nums[i];
            counts[h] = 0;
        }
        counts[h] += 1;
    }
    size_t full = ((size_t)1 << m) - 1;
    int64_t *want = calloc(full + 1, sizeof(int64_t));
    for (size_t mask = 1; mask <= full; mask++) {
        int low = __builtin_ctzll(mask);
        want[mask] = want[mask & (mask - 1)] + quantity[low];
    }
    bool *can = calloc(full + 1, sizeof(bool));
    bool *before = malloc(full + 1);
    can[0] = true;
    for (int s = 0; s < SLOTS; s++) {
        if (!used[s]) continue;
        int64_t count = counts[s];
        memcpy(before, can, full + 1);
        for (size_t mask = 0; mask <= full; mask++) {
            if (!before[mask]) continue;
            size_t rest = full & ~mask;
            size_t sub = rest;
            while (sub > 0) {
                if (want[sub] <= count) can[mask | sub] = true;
                sub = (sub - 1) & rest;
            }
        }
    }
    bool answer = can[full];
    free(want);
    free(can);
    free(before);
    return answer;
}

static int64_t seed = 1655;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t nums[PROBLEMS][N];
    static int32_t quantity[PROBLEMS][M];
    for (int p = 0; p < PROBLEMS; p++) {
        for (int i = 0; i < N; i++) nums[p][i] = (int32_t)(next_random() % 50 + 1);
        for (int i = 0; i < M; i++) quantity[p][i] = (int32_t)(next_random() % 3000 + 1);
    }
    int64_t check = 0, served = 0;
    for (int p = 0; p < PROBLEMS; p++) {
        bool answer = can_distribute(nums[p], N, quantity[p], M);
        if (answer) served += 1;
        check = (check * 31 + (answer ? 2 : 1)) % 1000000007;
    }
    printf("200 problems of 100000 numbers and 10 customers: %lld served, checksum %lld\n", (long long)served, (long long)check);
    return 0;
}
