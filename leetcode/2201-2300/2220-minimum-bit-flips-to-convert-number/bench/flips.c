// LeetCode #2220: Minimum Bit Flips to Convert Number -- bench mirror of
// flips.kara: the 1 bits of start ^ goal, counted by clearing the lowest
// with x & (x - 1).
#include <stdio.h>

static long min_bit_flips(long start, long goal) {
    long differ = start ^ goal;
    long flips = 0;
    while (differ != 0) {
        differ &= differ - 1;
        flips++;
    }
    return flips;
}

static long seed = 2220;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// a draw of 30 bits, since one draw stops at 32767
static long wide_random(void) {
    long high = next_random();
    return high * 32768 + next_random();
}

#define N 100000
static long starts[N], goals[N];

int main(void) {
    // 10^5 pairs up to 10^9
    for (long i = 0; i < N; i++) {
        starts[i] = wide_random() % 1000000001;
        goals[i] = wide_random() % 1000000001;
    }
    long check = 0;
    for (long r = 0; r < 50; r++) {
        // punch: one goal is drawn again before each round
        goals[r * 1999] = wide_random() % 1000000001;
        long total = 0;
        for (long i = 0; i < N; i++) total += min_bit_flips(starts[i], goals[i]);
        check = (check * 31 + total) % 1000000007;
    }
    printf("10^5 pairs, 50 punches: checksum %ld\n", check);
    return 0;
}
