// Benchmark for #828: Count Unique Characters of All Substrings of a Given
// String -- the ★ arm (each character's contribution).
//
// Mirrors unique_letter_string.kara: a character at i is unique in
// (i - prev) * (next - i) substrings, prev and next the copies of its
// letter beside it; one pass keeps the last two positions of each letter
// and settles the middle one each time a letter recurs.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t unique_letter_string(const char *s, int64_t n) {
    int64_t last[26], before[26];
    for (int c = 0; c < 26; c++) last[c] = before[c] = -1;
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t c = s[i] - 'A';
        if (last[c] >= 0) total += (last[c] - before[c]) * (i - last[c]);
        before[c] = last[c];
        last[c] = i;
    }
    for (int c = 0; c < 26; c++)
        if (last[c] >= 0) total += (last[c] - before[c]) * (n - last[c]);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 32, rounds = 12800, n = 100000;
    int64_t seed = 828;
    char *strings[32];
    for (int64_t g = 0; g < count; g++) {
        int64_t letters = 1 + g % 26;
        strings[g] = malloc((size_t)n);
        for (int64_t i = 0; i < n; i++) strings[g][i] = (char)('A' + next_random(&seed) % letters);
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t r = unique_letter_string(strings[round % count], n);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    printf("%lld rounds of %lld strings: total %lld, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) free(strings[g]);
    return 0;
}
