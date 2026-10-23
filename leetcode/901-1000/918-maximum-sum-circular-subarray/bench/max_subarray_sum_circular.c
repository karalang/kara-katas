// LeetCode #918: Maximum Sum Circular Subarray -- bench: C mirror of
// Kadane for the largest and the smallest sum in
// max_subarray_sum_circular.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_subarray_sum_circular(const int64_t *nums, int64_t n) {
    int64_t total = 0, best_here = 0, best = nums[0], worst_here = 0, worst = nums[0];
    for (int64_t k = 0; k < n; k++) {
        int64_t v = nums[k];
        total += v;
        best_here = v > best_here + v ? v : best_here + v;
        if (best_here > best)
            best = best_here;
        worst_here = v < worst_here + v ? v : worst_here + v;
        if (worst_here < worst)
            worst = worst_here;
    }
    if (best < 0)
        return best;
    return best > total - worst ? best : total - worst;
}

static int64_t seed = 918;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t value(void) {
    int64_t high = next_random();
    return (high * 2 + next_random() % 2) % 60001 - 30000;
}

int main(void) {
    int64_t rounds = 4000;
    int64_t n = 30000;
    int64_t *nums = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++)
        nums[i] = value();
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t i = next_random() % n;
        int64_t old = nums[i];
        nums[i] = value();
        int64_t a = max_subarray_sum_circular(nums, n);
        total += a;
        check = (check * 1000003 + a) % 1000000007;
        nums[i] = old;
    }
    printf("%lld rounds over %lld values: answers summing to %lld, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)check);
    free(nums);
    return 0;
}
