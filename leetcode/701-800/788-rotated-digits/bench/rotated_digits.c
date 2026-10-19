// LeetCode 788 — Rotated Digits: the bench, in C.
// Mirrors rotated_digits.kara: every number up to n checked digit by
// digit, for 50,000 random n.
#include <stdint.h>
#include <stdio.h>

static int64_t rotated_digits(int64_t n) {
    int64_t good = 0;
    for (int64_t x = 1; x <= n; x++) {
        int64_t rest = x;
        int valid = 1, changed = 0;
        while (rest > 0) {
            int64_t d = rest % 10;
            if (d == 3 || d == 4 || d == 7) {
                valid = 0;
                break;
            }
            if (d == 2 || d == 5 || d == 6 || d == 9) changed = 1;
            rest /= 10;
        }
        if (valid && changed) good++;
    }
    return good;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 788, rounds = 50000, sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t n = 1 + next_random(&seed) % 10000;
        int64_t good = rotated_digits(n);
        sum += good;
        check = (check * 31 + good) % 1000000007;
    }
    printf("%lld rounds of n up to 10000: answers sum to %lld, checksum %lld\n", (long long)rounds, (long long)sum,
           (long long)check);
    return 0;
}
