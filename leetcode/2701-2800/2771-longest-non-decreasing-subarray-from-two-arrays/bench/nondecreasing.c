// LeetCode #2771: Longest Non-decreasing Subarray From Two Arrays -- the
// bench in C: the ★ arm over 20 pairs of 10^5 numbers, all drawn first,
// then each answered 10 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 20
#define N 100000

static int64_t seed = 2771;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t imax(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t max_non_decreasing_length(const int64_t *nums1, const int64_t *nums2, int64_t n) {
    int64_t one = 1, two = 1, best = 1;
    for (int64_t i = 1; i < n; i++) {
        int64_t next_one = 1, next_two = 1;
        if (nums1[i - 1] <= nums1[i]) next_one = imax(next_one, one + 1);
        if (nums2[i - 1] <= nums1[i]) next_one = imax(next_one, two + 1);
        if (nums1[i - 1] <= nums2[i]) next_two = imax(next_two, one + 1);
        if (nums2[i - 1] <= nums2[i]) next_two = imax(next_two, two + 1);
        one = next_one;
        two = next_two;
        best = imax(imax(best, one), two);
    }
    return best;
}

static int64_t a1[COUNT][N], a2[COUNT][N];

int main(void) {
    int rounds = 10;
    for (int c = 0; c < COUNT; c++) {
        int64_t noise = next_random() % 200 + 1;
        for (int64_t i = 0; i < N; i++) a1[c][i] = i * 10 + next_random() % noise + 1;
        for (int64_t i = 0; i < N; i++) a2[c][i] = wide() % 1000000000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = max_non_decreasing_length(a1[c], a2[c], N);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d pairs of 10^5, %d rounds: lengths sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
