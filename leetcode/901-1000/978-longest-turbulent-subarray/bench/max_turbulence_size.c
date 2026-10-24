// Benchmark: LeetCode #978 Longest Turbulent Subarray -- the ★ arm, two
// running lengths, on 20 arrays of 40000 values. Mirrors
// max_turbulence_size.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>

#define N 40000
#define COUNT 20

static int64_t max_turbulence_size(const int64_t *arr, int64_t n) {
    int64_t best = 1, up = 1, down = 1;
    for (int64_t i = 1; i < n; i++) {
        if (arr[i - 1] < arr[i]) {
            up = down + 1;
            down = 1;
        } else if (arr[i - 1] > arr[i]) {
            down = up + 1;
            up = 1;
        } else {
            up = 1;
            down = 1;
        }
        int64_t m = up > down ? up : down;
        if (m > best) best = m;
    }
    return best;
}

static int64_t seed = 978;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t arrays[COUNT][N];

int main(void) {
    int64_t rounds = 150;
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < N; i++) arrays[c][i] = next_random() % 100;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t k = max_turbulence_size(arrays[(r + i) % COUNT], N);
            total += k;
            check = (check * 31 + k) % 1000000007;
        }
    }
    printf("%lld rounds over %d arrays of 40000 values: lengths total %lld, checksum %lld\n",
           (long long)rounds, COUNT, (long long)total, (long long)check);
    return 0;
}
