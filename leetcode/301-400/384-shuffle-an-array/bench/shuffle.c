// Benchmark for #384: mirror of shuffle.kara (Fisher-Yates from the end).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *original;
    int64_t n;
    int64_t seed;
} Solution;

static int64_t below(Solution *s, int64_t n) {
    s->seed = (s->seed * 1103515245 + 12345) % 2147483648LL;
    return (s->seed / 65536) % n;
}

static int64_t *shuffle(Solution *s) {
    int64_t *a = malloc(s->n * sizeof(int64_t));
    memcpy(a, s->original, s->n * sizeof(int64_t));
    for (int64_t i = s->n - 1; i > 0; i--) {
        int64_t j = below(s, i + 1);
        int64_t t = a[i];
        a[i] = a[j];
        a[j] = t;
    }
    return a;
}

int main(void) {
    int64_t n = 1000;
    int64_t *nums = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) nums[i] = i * 7 % 1000;
    Solution s = {nums, n, 384};
    int64_t checksum = 0;
    for (int q = 0; q < 250000; q++) {
        int64_t *a = shuffle(&s);
        int64_t sum = 0;
        for (int64_t k = 0; k < n; k++) sum += a[k] * (k + 1);
        checksum = (checksum * 31 + sum) % 1000000007;
        free(a);
    }
    printf("250000 shuffles of 1000 values, checksum %lld\n", (long long)checksum);
    free(nums);
    return 0;
}
