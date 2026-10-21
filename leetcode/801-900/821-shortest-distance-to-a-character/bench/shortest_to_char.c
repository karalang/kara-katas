// Benchmark for #821: Shortest Distance to a Character -- the ★ arm (two sweeps).
//
// Mirrors shortest_to_char.kara: the characters copied out as 32-bit
// code points, as the Kāra program collects its `chars()`; a sweep from
// the left keeps the last `c` seen and a sweep from the right the first,
// and each place keeps the nearer of the two.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// The strings are ASCII, so each byte is one code point.
static int64_t *shortest_to_char(const char *s, int64_t n, uint32_t c) {
    uint32_t *chars = malloc((size_t)n * sizeof(uint32_t));
    for (int64_t i = 0; i < n; i++) chars[i] = (unsigned char)s[i];
    int64_t *answer = malloc((size_t)n * sizeof(int64_t));
    int64_t last = -n;
    for (int64_t i = 0; i < n; i++) {
        if (chars[i] == c) last = i;
        answer[i] = i - last;
    }
    last = 2 * n;
    for (int64_t i = n - 1; i >= 0; i--) {
        if (chars[i] == c) last = i;
        if (last - i < answer[i]) answer[i] = last - i;
    }
    free(chars);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 64;
    int64_t rounds = 50000;
    int64_t seed = 821;
    char *strings[64];
    uint32_t targets[64];
    for (int64_t g = 0; g < count; g++) {
        strings[g] = malloc(10001);
        for (int64_t i = 0; i < 10000; i++) strings[g][i] = (char)('a' + next_random(&seed) % 26);
        strings[g][10000] = '\0';
        targets[g] = (uint32_t)('a' + next_random(&seed) % 26);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        int64_t *answer = shortest_to_char(strings[g], 10000, targets[g]);
        for (int64_t i = 0; i < 10000; i++) total += answer[i];
        checksum = (checksum * 131 + answer[round % 10000]) % 1000000007;
        free(answer);
    }
    printf("%lld rounds of %lld strings: total %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
