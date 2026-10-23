// LeetCode #902: Numbers At Most N Given Digit Set -- bench program, C.
//
// Lengths, then the digits of n from the left, asked about every one of
// the 511 sets of the digits 1 to 9, built once, in turn, each time with a
// random n from 1 to 10^9, and the counts folded into a checksum.

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static const char *names[9] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"};

static int64_t at_most_n_given_digit_set(const char **digits, int64_t d, int64_t n) {
    char s[24];
    int64_t k = snprintf(s, sizeof s, "%lld", (long long)n);
    int64_t count = 0;
    int64_t power = 1;
    for (int64_t j = 1; j < k; j++) {
        power *= d;
        count += power;
    }
    for (int64_t i = 0; i < k; i++) {
        int64_t rest = k - i - 1;
        int64_t ways = 1;
        for (int64_t j = 0; j < rest; j++) {
            ways *= d;
        }
        int64_t smaller = 0;
        int equal = 0;
        for (int64_t j = 0; j < d; j++) {
            char c = digits[j][0];
            if (c < s[i]) {
                smaller += 1;
            } else if (c == s[i]) {
                equal = 1;
            }
        }
        count += smaller * ways;
        if (!equal) {
            return count;
        }
    }
    return count + 1;
}

static int64_t seed = 902;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t queries = 8000000;
    const char *sets[511][9];
    int64_t sizes[511];
    for (int64_t mask = 1; mask < 512; mask++) {
        int64_t d = 0;
        for (int64_t c = 1; c < 10; c++) {
            if (((mask >> (c - 1)) & 1) == 1) {
                sets[mask - 1][d++] = names[c - 1];
            }
        }
        sizes[mask - 1] = d;
    }
    int64_t check = 0;
    int64_t total = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t hi = next_random();
        int64_t lo = next_random();
        int64_t n = 1 + (hi * 32768 + lo) % 1000000000;
        int64_t got = at_most_n_given_digit_set(sets[q % 511], sizes[q % 511], n);
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    printf("%lld queries over the 511 digit sets: counts summing to %lld, checksum %lld\n",
           (long long)queries, (long long)total, (long long)check);
    return 0;
}
