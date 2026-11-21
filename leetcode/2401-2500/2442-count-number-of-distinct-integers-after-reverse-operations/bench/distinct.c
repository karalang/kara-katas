// LeetCode #2442: Count Number of Distinct Integers After Reverse
// Operations -- the bench, the ★ arm: the digits reversed by `% 10` and
// `/ 10`, and a table of flags up to the largest value. The list of
// values and the table are allocated for each answer, as the other
// languages' are.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t reversed(int64_t x) {
    int64_t r = 0, y = x;
    while (y > 0) {
        r = r * 10 + y % 10;
        y /= 10;
    }
    return r;
}

static int64_t count_distinct_integers(const int64_t *nums, int64_t n) {
    int64_t *values = malloc(2 * n * sizeof(int64_t));
    memcpy(values, nums, n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) values[n + i] = reversed(nums[i]);
    int64_t largest = 0;
    for (int64_t i = 0; i < 2 * n; i++)
        if (values[i] > largest) largest = values[i];
    bool *seen = calloc(largest + 1, sizeof(bool));
    int64_t count = 0;
    for (int64_t i = 0; i < 2 * n; i++)
        if (!seen[values[i]]) {
            seen[values[i]] = true;
            count++;
        }
    free(seen);
    free(values);
    return count;
}

static int64_t seed = 2442;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return 1 + (a * 32768 + next_random()) % 1000000;
}

int main(void) {
    int64_t *arrays[4];
    for (int c = 0; c < 4; c++) {
        arrays[c] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) arrays[c][i] = wide();
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 40; p++)
        for (int64_t c = 0; c < 4; c++) {
            int64_t at = (p * 7919 + c * 104729) % 100000;
            arrays[c][at] = wide();
            check = (check * 31 + count_distinct_integers(arrays[c], 100000) + p) % 1000000007;
        }
    printf("40 passes over 4 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int c = 0; c < 4; c++) free(arrays[c]);
    return 0;
}
