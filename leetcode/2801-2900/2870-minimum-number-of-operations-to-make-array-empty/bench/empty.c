// LeetCode #2870: Minimum Number of Operations to Make Array Empty --
// the bench, as empty.kara: 50 arrays of 10^5 values, each answered 10
// times by the sorted-runs arm. The sort is qsort on a copy made each
// call, as the other languages sort a fresh copy.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_value(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t min_operations(const int64_t *nums, int64_t n) {
    int64_t *sorted = malloc(n * sizeof *sorted);
    memcpy(sorted, nums, n * sizeof *sorted);
    qsort(sorted, n, sizeof *sorted, by_value);
    int64_t ops = 0;
    for (int64_t i = 0; i < n;) {
        int64_t j = i;
        while (j < n && sorted[j] == sorted[i]) j++;
        int64_t f = j - i;
        if (f == 1) {
            free(sorted);
            return -1;
        }
        ops += (f + 2) / 3;
        i = j;
    }
    free(sorted);
    return ops;
}

static int64_t seed = 2870;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 50, rounds = 10, n = 100000;
    int64_t *arrays = malloc(count * n * sizeof *arrays);
    for (int64_t c = 0; c < count; c++) {
        int64_t *nums = arrays + c * n, len = 0;
        while (len < n) {
            int64_t v = wide() % 1000000 + 1;
            int64_t copies = next_random() % 7 + 2;
            if (copies > n - len) copies = n - len;
            for (int64_t k = 0; k < copies; k++) nums[len++] = v;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = wide() % (i + 1), t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t ops = min_operations(arrays + c * n, n);
            total += ops;
            check = (check * 31 + ops + 1 + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: %lld operations, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
