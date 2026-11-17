// LeetCode #2222: Number of Ways to Select Buildings -- bench mirror of
// buildings.kara: one pass keeping the 0s and 1s behind and the pairs
// "01" and "10", each character closing the pairs it completes.
#include <stdio.h>
#include <string.h>

#define A 30
#define N 100000

static long number_of_ways(const char *s) {
    long zeros = 0, ones = 0, zero_ones = 0, one_zeros = 0, ways = 0;
    for (; *s; s++) {
        if (*s == '0') {
            ways += zero_ones;
            one_zeros += ones;
            zeros++;
        } else {
            ways += one_zeros;
            zero_ones += zeros;
            ones++;
        }
    }
    return ways;
}

static long seed = 2222;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char streets[A][N];
static char s[N + 1];

int main(void) {
    // 10^5 buildings, each a 1 with chance one half
    for (int a = 0; a < A; a++)
        for (long i = 0; i < N; i++) streets[a][i] = next_random() % 2 == 1 ? '1' : '0';
    long check = 0;
    for (int a = 0; a < A; a++)
        for (long r = 0; r < 10; r++) {
            // punch: one building is drawn again before each answer
            streets[a][r * 9999] = next_random() % 2 == 1 ? '1' : '0';
            memcpy(s, streets[a], N);
            s[N] = 0;
            check = (check * 31 + number_of_ways(s)) % 1000000007;
        }
    printf("30 streets of 10^5, 10 punches: checksum %ld\n", check);
    return 0;
}
