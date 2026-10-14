// Benchmark for #581: C mirror of the ★ arm (two sweeps); see
// find_unsorted_subarray.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_unsorted_subarray(const int64_t *nums, int64_t n) {
    int64_t largest = nums[0];
    int64_t end = -1;
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] < largest) {
            end = i;
        } else {
            largest = nums[i];
        }
    }
    int64_t smallest = nums[n - 1];
    int64_t start = 0;
    for (int64_t i = n - 2; i >= 0; i--) {
        if (nums[i] > smallest) {
            start = i;
        } else {
            smallest = nums[i];
        }
    }
    return end == -1 ? 0 : end - start + 1;
}

// ---- benchmark --------------------------------------------------------------

static int64_t seed = 581;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random() * 32768;
    return high + next_random();
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int64_t count = 100;
    int64_t rounds = 600;
    int64_t *cases[100];
    for (int64_t g = 0; g < count; g++) {
        int64_t *nums = malloc(10000 * sizeof(int64_t));
        for (int64_t i = 0; i < 10000; i++) {
            nums[i] = wide() % 200001 - 100000;
        }
        qsort(nums, 10000, sizeof(int64_t), cmp);
        int64_t swaps = 1 + next_random() % 3;
        for (int64_t s = 0; s < swaps; s++) {
            int64_t i = wide() % 10000;
            int64_t j = wide() % 10000;
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
        cases[g] = nums;
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int64_t got = find_unsorted_subarray(cases[p], 10000);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%lld arrays of 10000 values, %lld rounds: total %lld, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free(cases[g]);
    }
    return 0;
}
