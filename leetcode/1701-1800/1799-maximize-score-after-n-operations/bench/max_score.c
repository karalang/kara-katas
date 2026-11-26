// LeetCode #1799: Maximize Score After N Operations -- the bench in C: the
// ★ arm over 100 random lists of 14 numbers built once, 100 calls.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t gcd(int32_t a, int32_t b) { return b == 0 ? a : gcd(b, a % b); }

static int32_t max_score(const int32_t *nums, int64_t m) {
    int64_t full = (int64_t)1 << m;
    int32_t *best = calloc(full, sizeof(int32_t));
    for (int64_t mask = 0; mask < full; mask++) {
        int64_t taken = __builtin_popcountll(mask);
        if (taken % 2 == 1) continue;
        int32_t op = (int32_t)(taken / 2 + 1);
        for (int64_t i = 0; i < m; i++) {
            if (mask >> i & 1) continue;
            for (int64_t j = i + 1; j < m; j++) {
                if (mask >> j & 1) continue;
                int64_t next = mask | (int64_t)1 << i | (int64_t)1 << j;
                int32_t s = best[mask] + op * gcd(nums[i], nums[j]);
                if (s > best[next]) best[next] = s;
            }
        }
    }
    int32_t r = best[full - 1];
    free(best);
    return r;
}

static int64_t seed = 1799;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[100][14];
    for (int l = 0; l < 100; l++)
        for (int x = 0; x < 14; x++) lists[l][x] = (int32_t)(1 + next_random() % 1000000);
    int64_t check = 0;
    for (int64_t call = 0; call < 100; call++) {
        check = (check * 31 + max_score(lists[(check + call) % 100], 14)) % 1000000007;
    }
    printf("100 calls over 100 lists of 14 numbers: checksum %lld\n", (long long)check);
    return 0;
}
