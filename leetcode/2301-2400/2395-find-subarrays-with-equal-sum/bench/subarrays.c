// LeetCode #2395: Find Subarrays With Equal Sum -- the bench, the ★ arm in
// C: each neighbouring pair's sum into an open-addressing hash set, a sum
// already there the answer.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000
#define SLOTS 4096

static int64_t seed = 2395;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static int find_subarrays(const int64_t *nums, int64_t n) {
    static int64_t keys[SLOTS];
    static char used[SLOTS];
    memset(used, 0, sizeof(used));
    for (int64_t i = 1; i < n; i++) {
        int64_t sum = nums[i - 1] + nums[i];
        uint64_t h = (uint64_t)sum * 0x9E3779B97F4A7C15ULL;
        size_t at = (size_t)(h >> 52) & (SLOTS - 1);
        while (used[at]) {
            if (keys[at] == sum) return 1;
            at = (at + 1) & (SLOTS - 1);
        }
        used[at] = 1;
        keys[at] = sum;
    }
    return 0;
}

int main(void) {
    static int64_t arrays[100][N];
    for (int a = 0; a < 100; a++) {
        int64_t top = 1000 + wide() % 1000000;
        for (int i = 0; i < N; i++) arrays[a][i] = wide() % (2 * top + 1) - top;
    }
    int64_t check = 0, yes = 0;
    for (int64_t p = 0; p < 2000; p++) {
        for (int a = 0; a < 100; a++) {
            int found = find_subarrays(arrays[a], N);
            check = (check * 31 + (found ? 2 : 1) + p) % 1000000007;
            if (found) yes++;
        }
    }
    printf("2000 passes over 100 arrays of 1000 values: checksum %lld, %lld yes\n", (long long)check, (long long)yes);
    return 0;
}
