// LeetCode #2006: Count Number of Pairs With Absolute Difference K -- the
// benchmark's C twin, the same algorithm as pairs.kara here, the counts
// allocated per call as the Kāra program does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_k_difference(const int64_t *nums, int n, int64_t k) {
    int64_t *seen = calloc(101, sizeof(int64_t));
    int64_t pairs = 0;
    for (int i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (x - k >= 1) pairs += seen[x - k];
        if (x + k <= 100) pairs += seen[x + k];
        seen[x]++;
    }
    free(seen);
    return pairs;
}

static int64_t seed = 2006;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 20000 arrays of 200 values up to 100 built once, then the ★ arm on
    // each for 25 rounds, k moving with the round
    enum { A = 20000, N = 200 };
    static int64_t arrays[A][N];
    for (int a = 0; a < A; a++)
        for (int i = 0; i < N; i++) arrays[a][i] = next_random() % 100 + 1;
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t r = 0; r < 25; r++) {
        for (int64_t a = 0; a < A; a++) {
            int64_t k = (r * 37 + a) % 99 + 1;
            int64_t answer = count_k_difference(arrays[a], N, k);
            calls++;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
