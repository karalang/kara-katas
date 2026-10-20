// LeetCode 813 -- Largest Sum of Averages: the bench, with the ★ arm's one
// row of prefix-sum DP.
#include <stdint.h>
#include <stdio.h>

static int64_t seed = 813;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static double largest_sum_of_averages(const int64_t *nums, int64_t n, int64_t k) {
    int64_t prefix[101];
    double best[101];
    prefix[0] = 0;
    for (int64_t i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    best[0] = 0.0;
    for (int64_t i = 1; i <= n; i++) {
        best[i] = (double)prefix[i] / (double)i;
    }
    for (int64_t g = 1; g < k; g++) {
        for (int64_t i = n; i >= 1; i--) {
            for (int64_t p = 1; p < i; p++) {
                double candidate = best[p] + (double)(prefix[i] - prefix[p]) / (double)(i - p);
                if (candidate > best[i]) {
                    best[i] = candidate;
                }
            }
        }
    }
    return best[n];
}

// 64 arrays of 100 numbers from 1 to 10000 are made once. Each round writes
// a new number into one place of the next array and finds its largest sum
// of averages in at most k groups, k going round 1 to 100.
int main(void) {
    static int64_t arrays[64][100];
    for (int a = 0; a < 64; a++) {
        for (int i = 0; i < 100; i++) {
            arrays[a][i] = 1 + next_random() % 10000;
        }
    }
    int64_t rounds = 6000;
    double total = 0.0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t a = r % 64;
        arrays[a][r / 64 % 100] = 1 + next_random() % 10000;
        double answer = largest_sum_of_averages(arrays[a], 100, 1 + r % 100);
        total += answer;
        check = (check * 131 + (int64_t)(answer * 1000.0)) % 1000000007;
    }
    printf("%lld rounds of 100 numbers: total %.5f, checksum %lld\n",
           (long long)rounds, total, (long long)check);
    return 0;
}
