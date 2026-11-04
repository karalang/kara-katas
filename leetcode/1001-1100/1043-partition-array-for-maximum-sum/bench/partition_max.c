// LeetCode #1043: Partition Array for Maximum Sum -- bench, C mirror of
// partition_max.kara (the bottom-up table).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_sum_after_partitioning(const int64_t *arr, int64_t n, int64_t k) {
    int64_t *best = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 1; i <= n; i++) {
        int64_t largest = 0;
        for (int64_t j = 1; j <= k && j <= i; j++) {
            if (arr[i - j] > largest) largest = arr[i - j];
            int64_t offer = best[i - j] + largest * j;
            if (offer > best[i]) best[i] = offer;
        }
    }
    int64_t answer = best[n];
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 400, N = 500, ROUNDS = 40 };
    int64_t seed = 1043;
    static int64_t arrays[COUNT][N];
    int64_t ks[COUNT];
    for (int a = 0; a < COUNT; a++) {
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            arrays[a][i] = (hi * 32768 + lo) % 1000000001;
        }
        ks[a] = next_random(&seed) % 50 + 1;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < COUNT; a++) {
            int64_t answer = max_sum_after_partitioning(arrays[a], N, ks[a]);
            total += answer;
            check = (check * 131 + answer % 1000000007) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: total %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)check);
    return 0;
}
