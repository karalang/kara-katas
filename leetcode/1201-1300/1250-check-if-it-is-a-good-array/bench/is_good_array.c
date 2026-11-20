// LeetCode #1250 bench, in C: the ★ arm (Euclid's algorithm folded over
// the array, stopping once the divisor reaches 1) on 50 random arrays of
// 100000 values built once, every value sharing a factor from 2 to 1000
// and, in half of them, one value of no shared factor put in at a random
// place; each asked 20 times, every answer folded into a checksum.

#include <stdio.h>

#define ARRAYS 50
#define N 100000

static long long seed = 1250;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long big_random(void) {
    long long hi = next_random() * 32768;
    return hi + next_random();
}

static long long gcd(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

static int is_good_array(const long long *nums, int n) {
    long long g = 0;
    for (int i = 0; i < n; i++) {
        g = gcd(g, nums[i]);
        if (g == 1) return 1;
    }
    return g == 1;
}

static long long arrays[ARRAYS][N];

int main(void) {
    for (int t = 0; t < ARRAYS; t++) {
        long long factor = next_random() % 999 + 2;
        for (int i = 0; i < N; i++) arrays[t][i] = factor * (big_random() % (1000000000 / factor) + 1);
        if (t % 2 == 0) arrays[t][big_random() % N] = 999999937;
    }
    long long check = 0;
    for (int r = 0; r < 20; r++)
        for (int t = 0; t < ARRAYS; t++) {
            int yes = is_good_array(arrays[t], N);
            check = (check * 131 + (yes ? t + 1 : 0)) % 1000000007;
        }
    printf("20 rounds of 50 arrays of 100000 values: checksum %lld\n", check);
    return 0;
}
