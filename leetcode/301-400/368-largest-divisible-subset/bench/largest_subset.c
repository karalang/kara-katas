// Benchmark for #368 -- mirror of largest_subset.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int cmp(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

// Writes the answer to out and returns its length.
static int64_t largest_divisible_subset(const int64_t *nums, int64_t n, int64_t *out) {
    int64_t *a = malloc(n * sizeof *a), *size = malloc(n * sizeof *size), *next = malloc(n * sizeof *next);
    for (int64_t i = 0; i < n; i++) {
        a[i] = nums[i];
        size[i] = 1;
        next[i] = -1;
    }
    qsort(a, n, sizeof *a, cmp);
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t k = i + 1; k < n; k++) {
            if (a[k] % a[i] == 0 && size[k] + 1 > size[i]) {
                size[i] = size[k] + 1;
                next[i] = k;
            }
        }
    }
    int64_t start = 0;
    for (int64_t i = 1; i < n; i++)
        if (size[i] > size[start]) start = i;
    int64_t len = 0;
    for (int64_t at = start; at != -1; at = next[at]) out[len++] = a[at];
    free(a);
    free(size);
    free(next);
    return len;
}

int main(void) {
    int64_t seed = 368, total = 0, checksum = 0;
    int64_t nums[1000], out[1000];
    char *taken = malloc(100001);
    for (int s = 0; s < 200; s++) {
        for (int64_t i = 0; i <= 100000; i++) taken[i] = 0;
        int64_t n = 0;
        while (n < 1000) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t v = 1 + (high * 32768 + seed / 65536) % 100000;
            if (!taken[v]) {
                taken[v] = 1;
                nums[n++] = v;
            }
        }
        int64_t len = largest_divisible_subset(nums, n, out);
        total += len;
        for (int64_t i = 0; i < len; i++) checksum = (checksum * 31 + out[i]) % 1000000007;
    }
    free(taken);
    printf("%lld numbers in the answers, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
