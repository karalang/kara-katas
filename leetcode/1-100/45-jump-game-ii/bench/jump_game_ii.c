// LeetCode #45 bench mirror — C, the greedy range-expansion matcher (★).
//
// Mirrors bench/jump_game_ii.kara: one cursor with farthest/current_end/jumps scalars,
// collapsing the layered BFS into a single scan. Build a reachable array once, punch one slot
// per iteration, fold the jump count into a rolling checksum. Same workload + sink as every
// other mirror.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t jump(const int64_t *nums, int64_t n) {
    int64_t jumps = 0, current_end = 0, farthest = 0;
    for (int64_t i = 0; i < n - 1; i++) {
        if (i + nums[i] > farthest) {
            farthest = i + nums[i];
        }
        if (i == current_end) {
            jumps++;
            current_end = farthest;
        }
    }
    return jumps;
}

int main(void) {
    const int64_t total = 200000;
    const int64_t modulus = 1000000007;
    const int64_t n = 1000;

    int64_t *nums = (int64_t *)malloc((size_t)n * sizeof(int64_t));
    for (int64_t a = 0; a < n; a++) {
        nums[a] = 1 + (a % 4);
    }

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        nums[k % n] = 1 + (k % 9);
        int64_t ans = jump(nums, n);
        acc = (acc * 131 + ans) % modulus;
    }

    free(nums);
    printf("%lld\n", (long long)acc);
    return 0;
}
