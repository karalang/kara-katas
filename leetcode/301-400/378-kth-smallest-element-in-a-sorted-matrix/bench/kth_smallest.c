// Benchmark for #378: mirror of kth_smallest.kara. The matrix is one flat
// allocation, row-major.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 300

static int64_t count_at_most(const int64_t *m, int64_t x) {
    int64_t count = 0;
    int64_t row = N - 1, col = 0;
    while (row >= 0 && col < N) {
        if (m[row * N + col] <= x) {
            count += row + 1;
            col++;
        } else {
            row--;
        }
    }
    return count;
}

static int64_t kth_smallest(const int64_t *m, int64_t k) {
    int64_t lo = m[0], hi = m[N * N - 1];
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (count_at_most(m, mid) >= k)
            hi = mid;
        else
            lo = mid + 1;
    }
    return lo;
}

int main(void) {
    int64_t seed = 378, checksum = 0;
    int64_t *m = malloc(sizeof(int64_t) * N * N);
    for (int rep = 0; rep < 10; rep++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                seed = (seed * 1103515245 + 12345) % 2147483648LL;
                int64_t d = (seed / 65536) % 10000;
                int64_t v;
                if (i == 0 && j == 0)
                    v = -1000000000;
                else if (i == 0)
                    v = m[j - 1] + d;
                else if (j == 0)
                    v = m[(i - 1) * N] + d;
                else {
                    int64_t up = m[(i - 1) * N + j], left = m[i * N + j - 1];
                    v = (up > left ? up : left) + d;
                }
                m[i * N + j] = v;
            }
        }
        for (int q = 0; q < 10000; q++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t k = 1 + (seed / 65536) % (N * N);
            checksum = (checksum * 1009 + kth_smallest(m, k) + 1000000000) % 1000000007;
        }
    }
    free(m);
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
