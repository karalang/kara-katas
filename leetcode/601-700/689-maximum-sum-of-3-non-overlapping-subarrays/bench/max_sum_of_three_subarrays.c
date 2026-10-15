// LeetCode #689: Maximum Sum of 3 Non-Overlapping Subarrays -- best to
// each side. Bench.
//
// 100 arrays of 20,000 values from 1 to 65535, each with a k from 1 to
// 1,000, are built once; then 20 rounds answer every array.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void max_sum_of_three_subarrays(const int64_t *nums, int64_t n, int64_t k, int64_t out[3]) {
    int64_t count = n - k + 1;
    int64_t *w = malloc((size_t)count * sizeof(int64_t));
    int64_t sum = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        if (i >= k) {
            sum -= nums[i - k];
        }
        if (i >= k - 1) {
            w[i - k + 1] = sum;
        }
    }
    int64_t *left = malloc((size_t)count * sizeof(int64_t));
    int64_t best = 0;
    for (int64_t i = 0; i < count; i++) {
        if (w[i] > w[best]) {
            best = i;
        }
        left[i] = best;
    }
    int64_t *right = malloc((size_t)count * sizeof(int64_t));
    best = count - 1;
    for (int64_t i = count - 1; i >= 0; i--) {
        if (w[i] >= w[best]) {
            best = i;
        }
        right[i] = best;
    }
    int64_t top = -1;
    for (int64_t j = k; j < count - k; j++) {
        int64_t a = left[j - k];
        int64_t c = right[j + k];
        int64_t total = w[a] + w[j] + w[c];
        if (total > top) {
            top = total;
            out[0] = a;
            out[1] = j;
            out[2] = c;
        }
    }
    free(w);
    free(left);
    free(right);
}

static int64_t seed = 689;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 100, rounds = 20, n = 20000;
    int64_t *arrays[100];
    int64_t ks[100];
    for (int64_t c = 0; c < count; c++) {
        arrays[c] = malloc((size_t)n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            arrays[c][i] = 1 + next_random() % 65535;
        }
        ks[c] = 1 + next_random() % 1000;
    }
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t got[3];
            max_sum_of_three_subarrays(arrays[c], n, ks[c], got);
            sum = (sum * 31 + got[0] + got[1] + got[2] + r) % 1000000007;
        }
    }
    printf("%lld arrays answered, checksum %lld\n", (long long)(count * rounds), (long long)sum);
    for (int64_t c = 0; c < count; c++) {
        free(arrays[c]);
    }
    return 0;
}
