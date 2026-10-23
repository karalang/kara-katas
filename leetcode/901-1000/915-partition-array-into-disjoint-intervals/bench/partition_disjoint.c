// LeetCode #915: Partition Array into Disjoint Intervals -- bench: C mirror
// of the largest on the left against the smallest on the right in
// partition_disjoint.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t partition_disjoint(const int64_t *nums, int64_t n) {
    int64_t *least_after = malloc(sizeof(int64_t) * n);
    least_after[n - 1] = nums[n - 1];
    for (int64_t i = n - 1; i > 0; i--)
        least_after[i - 1] = nums[i - 1] < least_after[i] ? nums[i - 1] : least_after[i];
    int64_t most = nums[0];
    int64_t answer = n;
    for (int64_t k = 1; k < n; k++) {
        if (most <= least_after[k]) {
            answer = k;
            break;
        }
        if (nums[k] > most)
            most = nums[k];
    }
    free(least_after);
    return answer;
}

static int64_t seed = 915;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t high = next_random();
    return (high * 32768 + next_random()) % 1000001;
}

int main(void) {
    int64_t rounds = 2000;
    int64_t n = 100000;
    int64_t *nums = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) {
        int64_t v = big() % 500000;
        nums[i] = i < n / 2 ? v : 500000 + v;
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t i = big() % n;
        int64_t old = nums[i];
        nums[i] = big();
        int64_t k = partition_disjoint(nums, n);
        total += k;
        check = (check * 1000003 + k) % 1000000007;
        nums[i] = old;
    }
    printf("%lld rounds over %lld values: left sides summing to %lld, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)check);
    free(nums);
    return 0;
}
