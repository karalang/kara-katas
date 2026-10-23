// LeetCode #906: Super Palindromes -- bench program, C.
//
// The palindromic roots built from their first halves, over random ranges
// below 10^18 given as strings. Each query counts the super-palindromes in
// its range and folds the count into a checksum.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void reverse_into(char *out, const char *s, int64_t n) {
    for (int64_t k = 0; k < n; k++) out[k] = s[n - 1 - k];
    out[n] = 0;
}

static int64_t superpalindromes_in_range(const char *left, const char *right) {
    int64_t lo = strtoll(left, NULL, 10);
    int64_t hi = strtoll(right, NULL, 10);
    int64_t count = 0;
    char digits[32], back[32], joined[64], shown[32], mirrored[32];
    for (int odd = 1; odd >= 0; odd--) {
        int64_t half = 1;
        for (;;) {
            int64_t n = snprintf(digits, sizeof digits, "%lld", (long long)half);
            reverse_into(back, digits, n);
            const char *tail = odd ? back + 1 : back;
            snprintf(joined, sizeof joined, "%s%s", digits, tail);
            int64_t root = strtoll(joined, NULL, 10);
            if (root > hi / root) break;
            int64_t square = root * root;
            int64_t m = snprintf(shown, sizeof shown, "%lld", (long long)square);
            reverse_into(mirrored, shown, m);
            if (square >= lo && strcmp(shown, mirrored) == 0) count += 1;
            half += 1;
        }
    }
    return count;
}

static int64_t seed = 906;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t big_random(void) {
    int64_t a = next_random() * 32768 + next_random();
    int64_t b = next_random() * 32768 + next_random();
    return a * 1073741824 + b;
}

int main(void) {
    int64_t queries = 40;
    int64_t top = 1000000000000000000LL;
    int64_t total = 0, check = 0;
    char left[32], right[32];
    for (int64_t q = 0; q < queries; q++) {
        int64_t a = 1 + big_random() % (top - 1);
        int64_t b = 1 + big_random() % (top - 1);
        snprintf(left, sizeof left, "%lld", (long long)(a < b ? a : b));
        snprintf(right, sizeof right, "%lld", (long long)(a < b ? b : a));
        int64_t got = superpalindromes_in_range(left, right);
        total += got;
        check = (check * 31 + got) % 1000000007;
    }
    printf("%lld ranges below 10^18: counts summing to %lld, checksum %lld\n", (long long)queries,
           (long long)total, (long long)check);
    return 0;
}
