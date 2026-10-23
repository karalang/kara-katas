// LeetCode #926: Flip String to Monotone Increasing -- bench: one pass.
// Mirrors min_flips_mono_incr.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_flips_mono_incr(const char *s, int64_t len) {
    int64_t flips = 0, ones = 0;
    for (int64_t i = 0; i < len; i++) {
        if (s[i] == '1') ones++;
        else flips = flips + 1 < ones ? flips + 1 : ones;
    }
    return flips;
}

static int64_t seed = 926;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 20, count = 100, n = 100000;
    // count strings of n characters, built once, leaning from 0 to 1
    char **strings = malloc(count * sizeof(char *));
    for (int64_t i = 0; i < count; i++) {
        int64_t lean = i % 101;
        strings[i] = malloc(n);
        for (int64_t j = 0; j < n; j++) strings[i][j] = next_random() % 100 < lean ? '1' : '0';
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every string, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            int64_t a = min_flips_mono_incr(strings[(r + i) % count], n);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%lld rounds over %lld strings of %lld: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    for (int64_t i = 0; i < count; i++) free(strings[i]);
    free(strings);
    return 0;
}
