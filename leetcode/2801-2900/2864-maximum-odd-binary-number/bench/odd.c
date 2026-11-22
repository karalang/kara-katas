// LeetCode #2864: Maximum Odd Binary Number -- the bench, as odd.kara:
// 10000 strings of 100 bits, each answered 50 times, every answer folded
// into the checksum byte by byte. Each answer is a fresh allocation, as
// the other languages' strings are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *maximum_odd_binary_number(const char *s, int64_t n) {
    int64_t ones = 0;
    for (int64_t i = 0; i < n; i++) ones += s[i] == '1';
    char *out = malloc(n + 1);
    memset(out, '1', ones - 1);
    memset(out + ones - 1, '0', n - ones);
    out[n - 1] = '1';
    out[n] = 0;
    return out;
}

static int64_t seed = 2864;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 10000, rounds = 50, n = 100;
    char *strings = malloc(count * (n + 1));
    for (int64_t c = 0; c < count; c++) {
        char *bits = strings + c * (n + 1);
        for (int64_t i = 0; i < n; i++) bits[i] = next_random() % 3 == 0 ? '1' : '0';
        bits[next_random() % n] = '1';
        bits[n] = 0;
    }
    int64_t ones_total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            char *best = maximum_odd_binary_number(strings + c * (n + 1), n);
            int64_t h = (check + r) % 1000000007;
            for (int64_t i = 0; i < n; i++) {
                ones_total += best[i] == '1';
                h = (h * 31 + (unsigned char)best[i]) % 1000000007;
            }
            check = h;
            free(best);
        }
    }
    printf("%lld strings of %lld, %lld rounds: %lld ones, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)ones_total, (long long)check);
    free(strings);
    return 0;
}
