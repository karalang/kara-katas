// Benchmark for #645: mirror of set_mismatch.kara (the ★ arm: counting
// each value) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void find_error_nums(const int64_t *nums, int64_t n, int64_t out[2]) {
    int64_t *seen = calloc((size_t)(n + 1), sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        seen[nums[i]] += 1;
    }
    int64_t twice = 0, missing = 0;
    for (int64_t v = 1; v < n + 1; v++) {
        if (seen[v] == 2) {
            twice = v;
        } else if (seen[v] == 0) {
            missing = v;
        }
    }
    free(seen);
    out[0] = twice;
    out[1] = missing;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t *mismatched(int64_t n, int64_t *seed) {
    int64_t *nums = malloc((size_t)n * sizeof(int64_t));
    for (int64_t v = 1; v < n + 1; v++) {
        nums[v - 1] = v;
    }
    for (int64_t i = 0; i < n - 1; i++) {
        int64_t j = i + next_random(seed) % (n - i);
        int64_t t = nums[i];
        nums[i] = nums[j];
        nums[j] = t;
    }
    int64_t from = next_random(seed) % n;
    int64_t to = next_random(seed) % (n - 1);
    if (to >= from) {
        to += 1;
    }
    nums[to] = nums[from];
    return nums;
}

int main(void) {
    int64_t seed = 645;
    int64_t n = 100000;
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        arrays[a] = mismatched(n, &seed);
    }
    int64_t rounds = 2000;
    int64_t twice_sum = 0, missing_sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t got[2];
        find_error_nums(arrays[r % 20], n, got);
        twice_sum += got[0];
        missing_sum += got[1];
    }
    printf("%lld rounds over 20 arrays of 100000 values: copies add to %lld, missing values to %lld\n", (long long)rounds, (long long)twice_sum, (long long)missing_sum);
    for (int a = 0; a < 20; a++) {
        free(arrays[a]);
    }
    return 0;
}
