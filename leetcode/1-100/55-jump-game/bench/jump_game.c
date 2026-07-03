/* LeetCode #55 bench harness — C mirror of jump_game.kara (greedy forward max-reach, star).
 * See ../README.md section Benchmarks. Built with `clang -O3`. */
#include <stdio.h>
#include <stdlib.h>

static long can_jump_work(const long *nums, long n) {
    long farthest = 0;
    long i = 0;
    while (i < n) {
        if (i > farthest) {
            return i;
        }
        if (i + nums[i] > farthest) {
            farthest = i + nums[i];
        }
        if (farthest >= n - 1) {
            return i;
        }
        i += 1;
    }
    return i;
}

int main(void) {
    long total = 200000;
    long modulus = 1000000007;
    long n = 1000;

    long *nums = (long *)malloc((size_t)n * sizeof(long));
    for (long a = 0; a < n; a++) {
        nums[a] = 1 + (a % 4);
    }

    long acc = 0;
    for (long k = 0; k < total; k++) {
        nums[k % n] = 1 + (k % 9);
        long ans = can_jump_work(nums, n);
        acc = (acc * 131 + ans) % modulus;
    }

    printf("%ld\n", acc);
    free(nums);
    return 0;
}
