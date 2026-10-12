// Benchmark for #413: mirror of arithmetic_slices.kara (slices ending
// here).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t number_of_arithmetic_slices(const int64_t *nums, int64_t n) {
    int64_t ending = 0, total = 0;
    for (int64_t i = 2; i < n; i++) {
        if (nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]) {
            ending += 1;
            total += ending;
        } else {
            ending = 0;
        }
    }
    return total;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 60000;
    int64_t n = 5000, seed = 413, len = 1;
    int64_t *nums = malloc(n * sizeof *nums);
    nums[0] = 0;
    while (len < n) {
        int64_t diff = step(&seed) % 7 - 3;
        int64_t run = 1 + step(&seed) % 30;
        for (int64_t k = 0; k < run; k++) {
            if (len < n) {
                int64_t last = nums[len - 1];
                if (last + diff > 1000 || last + diff < -1000) {
                    diff = -diff;
                }
                nums[len++] = last + diff;
            }
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        nums[r * 7919 % n] += r % 3 - 1;
        int64_t answer = number_of_arithmetic_slices(nums, n);
        total += answer;
        checksum = (checksum * 31 + answer) % 1000000007;
    }
    printf("%lld rounds on %lld numbers: total %lld, checksum %lld\n", (long long)rounds, (long long)n, (long long)total, (long long)checksum);
    free(nums);
    return 0;
}
