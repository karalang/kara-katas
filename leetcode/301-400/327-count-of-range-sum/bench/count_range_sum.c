// Benchmark workload for LeetCode #327 — C mirror of count_range_sum.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 100000
#define PUNCHES 20
#define MODULUS 1073741789LL

static int64_t count_and_sort(int64_t *p, int64_t *tmp, int64_t lo, int64_t hi, int64_t lower, int64_t upper) {
    if (hi - lo <= 1) {
        return 0;
    }
    int64_t mid = lo + (hi - lo) / 2;
    int64_t count = count_and_sort(p, tmp, lo, mid, lower, upper) + count_and_sort(p, tmp, mid, hi, lower, upper);

    int64_t start = mid, end = mid;
    for (int64_t a = lo; a < mid; a++) {
        while (start < hi && p[start] < p[a] + lower) {
            start++;
        }
        while (end < hi && p[end] <= p[a] + upper) {
            end++;
        }
        count += end - start;
    }

    int64_t i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (p[i] <= p[j]) {
            tmp[k] = p[i];
            i++;
        } else {
            tmp[k] = p[j];
            j++;
        }
        k++;
    }
    while (i < mid) {
        tmp[k++] = p[i++];
    }
    while (j < hi) {
        tmp[k++] = p[j++];
    }
    for (int64_t t = lo; t < hi; t++) {
        p[t] = tmp[t];
    }
    return count;
}

static int64_t count_range_sum(const int64_t *nums, int64_t n, int64_t lower, int64_t upper) {
    int64_t *p = malloc((size_t)(n + 1) * sizeof *p);
    int64_t *tmp = calloc((size_t)(n + 1), sizeof *tmp);
    p[0] = 0;
    int64_t s = 0;
    for (int64_t i = 0; i < n; i++) {
        s += nums[i];
        p[i + 1] = s;
    }
    int64_t count = count_and_sort(p, tmp, 0, n + 1, lower, upper);
    free(p);
    free(tmp);
    return count;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 327;
    int64_t *a = malloc(LEN * sizeof *a);
    for (int64_t i = 0; i < LEN; i++) {
        a[i] = next(&seed) % 2001 - 1000;
    }
    int64_t sink = 0;
    for (int64_t r = 0; r < PUNCHES; r++) {
        int64_t pos = (next(&seed) * 32768 + next(&seed)) % LEN;
        a[pos] = next(&seed) % 2001 - 1000;
        int64_t w = next(&seed) % 1000;
        int64_t count = count_range_sum(a, LEN, -w, w);
        sink = (sink * 31 + count % MODULUS) % MODULUS;
    }
    printf("sink %lld\n", (long long)sink);
    free(a);
    return 0;
}
