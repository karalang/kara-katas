// LeetCode #416: Partition Equal Subset Sum -- C mirror of
// can_partition.kara (sums up to half). Usage: ./can_partition [rounds]
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool can_partition(const int64_t *nums, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += nums[i];
    }
    if (total % 2 != 0) {
        return false;
    }
    int64_t half = total / 2;
    bool *reach = calloc(half + 1, sizeof *reach);
    reach[0] = true;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        int64_t s = half;
        while (s >= x) {
            if (reach[s - x]) {
                reach[s] = true;
            }
            s -= 1;
        }
    }
    bool answer = reach[half];
    free(reach);
    return answer;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 2000;
    int64_t n = 200, seed = 416, total = 0;
    int64_t *nums = malloc(n * sizeof *nums);
    for (int64_t k = 0; k < n; k++) {
        nums[k] = 1 + step(&seed) % 100;
        total += nums[k];
    }
    if (total % 2 != 0) {
        nums[0] += nums[0] < 100 ? 1 : -1;
    }
    int64_t yes = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t i = step(&seed) % n;
        int64_t j = step(&seed) % n;
        if (nums[i] < 100 && nums[j] > 1) {
            nums[i] += 1;
            nums[j] -= 1;
        }
        bool answer = can_partition(nums, n);
        if (answer) {
            yes += 1;
        }
        checksum = (checksum * 31 + nums[i] + (answer ? r : 0)) % 1000000007;
    }
    printf("%lld rounds on %lld numbers: %lld can be split, checksum %lld\n", (long long)rounds, (long long)n, (long long)yes, (long long)checksum);
    free(nums);
    return 0;
}
