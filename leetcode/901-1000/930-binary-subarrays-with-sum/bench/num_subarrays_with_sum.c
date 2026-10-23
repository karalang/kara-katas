// LeetCode #930: Binary Subarrays With Sum -- bench: prefix sums counted
// in an array. Mirrors num_subarrays_with_sum.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_subarrays_with_sum(const int64_t *nums, int64_t n, int64_t goal) {
    int64_t *seen = calloc(n + 1, sizeof(int64_t));
    seen[0] = 1;
    int64_t sum = 0, count = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        if (sum >= goal) count += seen[sum - goal];
        seen[sum]++;
    }
    free(seen);
    return count;
}

static int64_t seed = 930;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 100, count = 100, n = 30000;
    // count arrays of n elements, built once, each leaning from 0 to 1 by
    // a random amount, with a goal from 0 to the number of 1s
    int64_t **arrays = malloc(count * sizeof(int64_t *));
    int64_t *goals = malloc(count * sizeof(int64_t));
    for (int64_t g = 0; g < count; g++) {
        int64_t lean = 1 + next_random() % 99;
        arrays[g] = malloc(n * sizeof(int64_t));
        int64_t ones = 0;
        for (int64_t i = 0; i < n; i++) {
            int64_t v = next_random() % 100 < lean ? 1 : 0;
            ones += v;
            arrays[g][i] = v;
        }
        goals[g] = next_random() % (ones + 1);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every array, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            int64_t p = (r + i) % count;
            int64_t a = num_subarrays_with_sum(arrays[p], n, goals[p]);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%lld rounds over %lld arrays of %lld: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    for (int64_t g = 0; g < count; g++) free(arrays[g]);
    free(arrays);
    free(goals);
    return 0;
}
