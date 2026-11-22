// LeetCode #2741: Special Permutations -- the bench (special.kara in C):
// ways[mask][last] carried forward to every partner of `last`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007LL

static int64_t special_perm(const int64_t *nums, int64_t n, int64_t *ways) {
    int64_t full = (1LL << n) - 1;
    memset(ways, 0, sizeof(int64_t) * (full + 1) * n);
    for (int64_t i = 0; i < n; i++) ways[(1LL << i) * n + i] = 1;
    for (int64_t mask = 1; mask < full; mask++) {
        for (int64_t last = 0; last < n; last++) {
            int64_t w = ways[mask * n + last];
            if (w == 0) continue;
            for (int64_t next = 0; next < n; next++) {
                if (((mask >> next) & 1) == 0 && (nums[next] % nums[last] == 0 || nums[last] % nums[next] == 0)) {
                    int64_t to = mask | (1LL << next);
                    ways[to * n + next] = (ways[to * n + next] + w) % MOD;
                }
            }
        }
    }
    int64_t total = 0;
    for (int64_t last = 0; last < n; last++) total = (total + ways[full * n + last]) % MOD;
    return total;
}

static int64_t seed = 2741;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 30, rounds = 5, n = 14;
    static const int64_t threes[4] = {1, 3, 9, 27};
    int64_t *arrays = malloc(sizeof(int64_t) * count * n);
    for (int64_t c = 0; c < count; c++) {
        int64_t len = 0;
        while (len < n) {
            int64_t a = next_random() % 6;
            int64_t b = next_random() % 4;
            int64_t x = (1LL << a) * threes[b];
            int seen = 0;
            for (int64_t i = 0; i < len; i++) seen |= arrays[c * n + i] == x;
            if (!seen) arrays[c * n + len++] = x;
        }
    }
    // a fresh table for each call, as the other languages allocate one
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t *ways = malloc(sizeof(int64_t) * (1LL << n) * n);
            int64_t k = special_perm(arrays + c * n, n, ways);
            free(ways);
            sum += k;
            check = (check * 31 + k + r) % 1000000007;
        }
    }
    printf("%lld arrays of 14 numbers, %lld rounds: counts sum to %lld, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)sum, (long long)check);
    free(arrays);
    return 0;
}
