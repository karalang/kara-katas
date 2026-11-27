// LeetCode #1838: Frequency of the Most Frequent Element -- the bench in C: the ★ arm over
// 200 calls on the first 50000 to 99999 of one list of 10^5 numbers from 1
// to 10^5, built once, with `k` from 1 to 10^5, each run's length and `k`
// drawn from the checksum so far. Each call copies its run, and the arm
// sorts a copy of its own.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t max_frequency(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *sorted = malloc(n * sizeof *sorted);
    memcpy(sorted, nums, n * sizeof *sorted);
    qsort(sorted, n, sizeof *sorted, by_value);
    int64_t best = 0, first = 0, sum = 0;
    for (int64_t last = 0; last < n; last++) {
        sum += sorted[last];
        while (sorted[last] * (last - first + 1) - sum > k) {
            sum -= sorted[first];
            first++;
        }
        if (last - first + 1 > best) best = last - first + 1;
    }
    free(sorted);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1838;
    int64_t *base = malloc(100000 * sizeof *base);
    for (int64_t i = 0; i < 100000; i++) {
        int64_t hi = next_random(&seed);
        base[i] = 1 + (hi * 32768 + next_random(&seed)) % 100000;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        int64_t n = 50000 + (check + call) % 50000;
        int64_t k = 1 + (check * 7 + call) % 100000;
        int64_t *run = malloc(n * sizeof *run);
        memcpy(run, base, n * sizeof *run);
        check = (check * 31 + max_frequency(run, n, k)) % 1000000007;
        free(run);
    }
    printf("200 calls: checksum %lld\n", (long long)check);
    return 0;
}
