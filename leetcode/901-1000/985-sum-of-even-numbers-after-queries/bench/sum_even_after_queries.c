// Benchmark: LeetCode #985 Sum of Even Numbers After Queries -- the ★ arm, a
// running sum, on LeetCode's largest: 10000 values and 10000 queries.
// Mirrors sum_even_after_queries.kara, .rs, .py and go-seq/.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 10000
#define Q 10000

// The answers in a fresh array of q sums, which the caller frees.
static int64_t *sum_even_after_queries(const int64_t *nums, int n, const int64_t *vals,
                                       const int64_t *index, int q) {
    int64_t *a = malloc(sizeof(int64_t) * n);
    memcpy(a, nums, sizeof(int64_t) * n);
    int64_t even = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] % 2 == 0) even += a[i];
    }
    int64_t *answer = malloc(sizeof(int64_t) * q);
    for (int k = 0; k < q; k++) {
        int64_t j = index[k];
        if (a[j] % 2 == 0) even -= a[j];
        a[j] += vals[k];
        if (a[j] % 2 == 0) even += a[j];
        answer[k] = even;
    }
    free(a);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t nums[20][N], vals[20][Q], idx[20][Q];

int main(void) {
    int64_t rounds = 300;
    int64_t seed = 985;
    for (int c = 0; c < 20; c++) {
        for (int i = 0; i < N; i++) nums[c][i] = next_random(&seed) % 20001 - 10000;
        for (int k = 0; k < Q; k++) {
            vals[c][k] = next_random(&seed) % 20001 - 10000;
            idx[c][k] = next_random(&seed) % 10000;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int c = (int)((r + i) % 20);
            int64_t *answer = sum_even_after_queries(nums[c], N, vals[c], idx[c], Q);
            int64_t last = answer[Q - 1];
            total += last;
            check = (check * 31 + (last % 1000000007 + 1000000007) % 1000000007) % 1000000007;
            free(answer);
        }
    }
    printf("%lld rounds over 20 cases of 10000 values and 10000 queries: sum %lld, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
