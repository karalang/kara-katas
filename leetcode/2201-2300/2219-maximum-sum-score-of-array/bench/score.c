// LeetCode #2219: Maximum Sum Score of Array -- bench mirror of
// score.kara: with the total known, one pass keeps the sum before i, and
// the sum from i on is the total less it.
#include <stdio.h>

static long maximum_sum_score(const long *nums, long n) {
    long total = 0;
    for (long i = 0; i < n; i++) total += nums[i];
    long before = 0;
    // no score is below the smaller of the first number and the total
    long best = nums[0] < total ? nums[0] : total;
    for (long i = 0; i < n; i++) {
        long from_here = total - before;
        before += nums[i];
        if (before > best) best = before;
        if (from_here > best) best = from_here;
    }
    return best;
}

static long seed = 2219;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// a draw of 30 bits, since one draw stops at 32767
static long wide_random(void) {
    long high = next_random();
    return high * 32768 + next_random();
}

#define A 30
#define N 100000
static long arrays[A][N];

int main(void) {
    // 10^5 numbers from -10^5 to 10^5
    for (int a = 0; a < A; a++)
        for (long i = 0; i < N; i++) arrays[a][i] = wide_random() % 200001 - 100000;
    long check = 0;
    for (int a = 0; a < A; a++)
        for (long r = 0; r < 10; r++) {
            // punch: one number is drawn again before each answer
            arrays[a][r * 9999] = wide_random() % 200001 - 100000;
            check = (check * 31 + maximum_sum_score(arrays[a], N) + 10000000000) % 1000000007;
        }
    printf("30 arrays of 10^5, 10 punches: checksum %ld\n", check);
    return 0;
}
