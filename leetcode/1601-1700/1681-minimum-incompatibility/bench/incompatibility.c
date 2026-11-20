// LeetCode #1681: Minimum Incompatibility -- the bench's C mirror: the ★ arm
// on 300 arrays of 16 values from 1 to 16, each with a random k that
// divides 16, all drawn first, each answered 4 times. The two tables are
// malloc'd for each answer, as the other languages allocate theirs.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAYS 300
#define N 16
#define ROUNDS 4

static int32_t minimum_incompatibility(const int32_t *nums, int64_t n, int32_t k) {
    int64_t size = n / k;
    int64_t full = ((int64_t)1 << n) - 1;
    int32_t *cost = malloc(((size_t)1 << n) * sizeof *cost);
    for (int64_t s = 0; s <= full; s++) {
        cost[s] = -1;
        if (__builtin_popcountll((unsigned long long)s) != size) continue;
        int64_t seen = 0;
        int32_t lo = INT32_MAX, hi = INT32_MIN;
        int ok = 1;
        for (int64_t i = 0; i < n; i++) {
            if (s >> i & 1) {
                int64_t bit = (int64_t)1 << nums[i];
                if (seen & bit) {
                    ok = 0;
                    break;
                }
                seen |= bit;
                if (nums[i] < lo) lo = nums[i];
                if (nums[i] > hi) hi = nums[i];
            }
        }
        if (ok) cost[s] = hi - lo;
    }
    const int32_t unreached = INT32_MAX;
    int32_t *best = malloc(((size_t)1 << n) * sizeof *best);
    for (int64_t m = 0; m <= full; m++) best[m] = unreached;
    best[0] = 0;
    for (int64_t m = 0; m < full; m++) {
        if (best[m] == unreached || __builtin_popcountll((unsigned long long)m) % size != 0) continue;
        int64_t free_ = full ^ m;
        int64_t lowest = free_ & -free_;
        for (int64_t s = free_; s > 0; s = (s - 1) & free_) {
            if ((s & lowest) && cost[s] >= 0 && best[m] + cost[s] < best[m | s]) best[m | s] = best[m] + cost[s];
        }
    }
    int32_t answer = best[full] == unreached ? -1 : best[full];
    free(cost);
    free(best);
    return answer;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1681;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t nums[ARRAYS][N];
    static int32_t ks[ARRAYS];
    static const int32_t divisors[5] = {1, 2, 4, 8, 16};
    for (int a = 0; a < ARRAYS; a++) {
        for (int i = 0; i < N; i++) nums[a][i] = (int32_t)(next_random() % N + 1);
        ks[a] = divisors[next_random() % 5];
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < ARRAYS; a++) {
            int64_t answer = minimum_incompatibility(nums[a], N, ks[a]);
            total += answer;
            check = (check * 31 + answer + 1 + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: answers sum to %lld, checksum %lld\n", ARRAYS, N, ROUNDS, (long long)total, (long long)check);
    return 0;
}
