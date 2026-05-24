/*
 * LeetCode 88 — two-pointer-from-back Merge Sorted Array, C mirror.
 * Algorithmic peer of bench/two_pointer.{kara,rs,py}. Same m, n, K,
 * maximally-alternating input, same sink formula.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static void merge(int64_t *nums1, int64_t m, const int64_t *nums2, int64_t n) {
    int64_t i = m - 1;
    int64_t j = n - 1;
    int64_t k = m + n - 1;
    while (j >= 0) {
        if (i >= 0 && nums1[i] > nums2[j]) {
            nums1[k] = nums1[i];
            i--;
        } else {
            nums1[k] = nums2[j];
            j--;
        }
        k--;
    }
}

int main(void) {
    const size_t M = 1000000;
    const size_t N = 1000000;
    const size_t TOTAL = M + N;

    int64_t *prefix_a = (int64_t *)malloc(M * sizeof(int64_t));
    int64_t *b = (int64_t *)malloc(N * sizeof(int64_t));
    int64_t *workspace = (int64_t *)malloc(TOTAL * sizeof(int64_t));

    for (size_t i = 0; i < M; i++) {
        prefix_a[i] = (int64_t)(2 * i);
    }
    for (size_t i = 0; i < N; i++) {
        b[i] = (int64_t)(2 * i + 1);
    }

    int64_t sum = 0;
    for (int iter = 0; iter < 10; iter++) {
        for (size_t p = 0; p < M; p++) {
            workspace[p] = prefix_a[p];
        }
        merge(workspace, (int64_t)M, b, (int64_t)N);
        sum += workspace[TOTAL - 1];
    }
    printf("%lld\n", (long long)sum);

    free(prefix_a);
    free(b);
    free(workspace);
    return 0;
}
