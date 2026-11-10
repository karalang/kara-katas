// LeetCode #2089: Find Target Indices After Sorting Array -- C mirror of
// the ★ arm's benchmark (target.kara): the same 10000 arrays, each asked for
// every target, two counts and the indices in a fresh `malloc`'d buffer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

static int64_t seed = 2089;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t *target_indices(const int64_t *nums, int n, int64_t target, int *len) {
    int64_t less = 0, equal = 0;
    for (int i = 0; i < n; i++)
        if (nums[i] < target) less++;
    for (int i = 0; i < n; i++)
        if (nums[i] == target) equal++;
    int64_t *out = malloc((equal > 0 ? equal : 1) * sizeof(int64_t));
    for (int64_t k = 0; k < equal; k++) out[k] = less + k;
    *len = (int)equal;
    return out;
}

int main(void) {
    int64_t(*arrays)[N] = malloc(10000 * sizeof(*arrays));
    for (int t = 0; t < 10000; t++)
        for (int i = 0; i < N; i++) arrays[t][i] = next_random() % 100 + 1;
    int64_t total = 0, check = 0;
    for (int t = 0; t < 10000; t++) {
        for (int64_t target = 1; target <= 100; target++) {
            int len;
            int64_t *got = target_indices(arrays[t], N, target, &len);
            for (int k = 0; k < len; k++) total += got[k] * target;
            check = (check * 31 + (int64_t)len * 100 + (len > 0 ? got[0] : 0)) % 1000000007;
            free(got);
        }
    }
    printf("1000000 answers: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(arrays);
    return 0;
}
