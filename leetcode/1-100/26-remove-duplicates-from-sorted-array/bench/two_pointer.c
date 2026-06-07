/*
 * LeetCode 26 — two-pointer in-place Remove Duplicates, C mirror.
 * Algorithmic peer of bench/two_pointer.{kara,rs,py}. Same N, K,
 * LCG-random-gap input, same sink formula.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t remove_duplicates(int64_t *nums, int64_t len) {
    if (len == 0) {
        return 0;
    }
    int64_t k = 1;
    for (int64_t i = 1; i < len; i++) {
        if (nums[i] != nums[k - 1]) {
            nums[k] = nums[i];
            k++;
        }
    }
    return k;
}

int main(void) {
    const size_t N = 2000000;

    int64_t *original = (int64_t *)calloc(N, sizeof(int64_t));
    int64_t *workspace = (int64_t *)calloc(N, sizeof(int64_t));

    int64_t state = 1;
    for (size_t i = 1; i < N; i++) {
        state = (state * 1103515245 + 12345) % 2147483648;
        original[i] = original[i - 1] + (state / 65536) % 2;
    }

    int64_t sum = 0;
    for (int iter = 0; iter < 10; iter++) {
        for (size_t p = 0; p < N; p++) {
            workspace[p] = original[p];
        }
        int64_t k = remove_duplicates(workspace, (int64_t)N);
        sum += k + workspace[k - 1];
    }
    printf("%lld\n", (long long)sum);

    free(original);
    free(workspace);
    return 0;
}
