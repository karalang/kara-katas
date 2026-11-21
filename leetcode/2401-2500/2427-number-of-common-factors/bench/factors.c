// LeetCode #2427: Number of Common Factors -- the bench, the ★ arm: the
// divisors of gcd(a, b), counted in pairs up to its square root.
#include <stdint.h>
#include <stdio.h>

static int64_t gcd(int64_t a, int64_t b) {
    while (b != 0) {
        int64_t r = a % b;
        a = b;
        b = r;
    }
    return a;
}

static int64_t common_factors(int64_t a, int64_t b) {
    int64_t g = gcd(a, b);
    int64_t count = 0;
    for (int64_t d = 1; d * d <= g; d++)
        if (g % d == 0) count += d * d == g ? 1 : 2;
    return count;
}

int main(void) {
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++)
        for (int64_t a = 1; a <= 1000; a++)
            for (int64_t b = 1; b <= 1000; b++) {
                int64_t other = (b + p - 1) % 1000 + 1;
                check = (check * 31 + common_factors(a, other) + p) % 1000000007;
            }
    printf("5 passes over 10^6 pairs: checksum %lld\n", (long long)check);
    return 0;
}
