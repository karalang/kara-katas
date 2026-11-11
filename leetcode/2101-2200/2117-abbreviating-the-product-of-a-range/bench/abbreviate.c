// LeetCode #2117: Abbreviating the Product of a Range -- the benchmark,
// the same algorithm as abbreviate.kara: the factors of 2 and 5 pulled
// out, the rest modulo 100000 and capped at 10^11, and a double of the
// leading digits.

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void abbreviate_product(int64_t left, int64_t right, char *out) {
    const int64_t cap = 100000000000LL;
    int64_t twos = 0, fives = 0, last = 1, exact = 1;
    double lead = 1.0;
    for (int64_t i = left; i <= right; i++) {
        int64_t x = i;
        while (x % 2 == 0) {
            x /= 2;
            twos++;
        }
        while (x % 5 == 0) {
            x /= 5;
            fives++;
        }
        last = last * x % 100000;
        exact = exact > cap / x ? cap : exact * x;
        lead *= (double)i;
        while (lead >= 1e12) {
            lead /= 10.0;
        }
    }
    int64_t zeros = twos < fives ? twos : fives;
    for (int64_t k = 0; k < twos - zeros; k++) {
        last = last * 2 % 100000;
        exact = exact > cap / 2 ? cap : exact * 2;
    }
    for (int64_t k = 0; k < fives - zeros; k++) {
        last = last * 5 % 100000;
        exact = exact > cap / 5 ? cap : exact * 5;
    }
    if (exact < 10000000000LL) {
        sprintf(out, "%llde%lld", (long long)exact, (long long)zeros);
        return;
    }
    while (lead >= 1e5) {
        lead /= 10.0;
    }
    sprintf(out, "%lld...%05llde%lld", (long long)lead, (long long)last, (long long)zeros);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2117, longs = 0, check = 0;
    char got[64];
    for (int t = 0; t < 40000; t++) {
        int64_t left = next_random(&seed) % 10000 + 1;
        int64_t right = left + next_random(&seed) % 3000;
        if (right > 10000) {
            right = 10000;
        }
        abbreviate_product(left, right, got);
        if (strstr(got, "...")) {
            longs++;
        }
        for (const char *p = got; *p; p++) {
            check = (check * 31 + (unsigned char)*p) % 1000000007;
        }
    }
    printf("40000 solves: %lld long answers, checksum %lld\n", (long long)longs, (long long)check);
    return 0;
}
