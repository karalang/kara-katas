// LeetCode #2740: Find the Value of the Partition -- the bench
// (partition.kara in C): sort a copy with qsort, and the least gap
// between neighbours.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t find_value_of_partition(int64_t *nums, int64_t n) {
    qsort(nums, n, sizeof(int64_t), cmp);
    int64_t best = INT64_MAX;
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] - nums[i - 1] < best) best = nums[i] - nums[i - 1];
    }
    return best;
}

static int64_t seed = 2740;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 20, n = 100000, rounds = 10;
    int64_t *arrays = malloc(sizeof(int64_t) * count * n);
    int64_t *work = malloc(sizeof(int64_t) * n);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            arrays[c * n + i] = (hi * 32768 + lo) % 1000000000 + 1;
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            memcpy(work, arrays + c * n, sizeof(int64_t) * n);
            int64_t value = find_value_of_partition(work, n);
            sum += value;
            check = (check * 31 + value + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld numbers, %lld rounds: values sum to %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)sum, (long long)check);
    free(arrays);
    free(work);
    return 0;
}
