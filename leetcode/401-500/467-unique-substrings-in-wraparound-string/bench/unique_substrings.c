// Benchmark for #467: mirror of unique_substrings.kara (the ★ arm: the
// longest run ending at each letter) on the same workload. Each string
// is a byte buffer with room for every letter the rounds append.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_substring_in_wrapround_string(const char *s, int64_t length) {
    int64_t longest[26] = {0};
    int64_t run = 0;
    int64_t previous = -1;
    for (int64_t i = 0; i < length; i++) {
        int64_t code = (int64_t)s[i] - 97;
        if (previous >= 0 && code == (previous + 1) % 26) {
            run += 1;
        } else {
            run = 1;
        }
        if (run > longest[code]) {
            longest[code] = run;
        }
        previous = code;
    }
    int64_t total = 0;
    for (int i = 0; i < 26; i++) {
        total += longest[i];
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char letter(int64_t i) {
    return (char)(97 + i % 26);
}

int main(void) {
    const int64_t count = 10;
    const int64_t n = 100000;
    const int64_t rounds = 100;
    int64_t seed = 467;
    char *strings[10];
    int64_t lengths[10];
    for (int64_t k = 0; k < count; k++) {
        char *s = malloc((size_t)(n + rounds));
        int64_t last = next_random(&seed) % 26;
        s[0] = letter(last);
        for (int64_t i = 1; i < n; i++) {
            if (next_random(&seed) % 16 == 0) {
                last = next_random(&seed) % 26;
            } else {
                last = (last + 1) % 26;
            }
            s[i] = letter(last);
        }
        strings[k] = s;
        lengths[k] = n;
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t k = 0; k < count; k++) {
            strings[k][lengths[k]++] = letter(next_random(&seed) % 26);
            int64_t found = find_substring_in_wrapround_string(strings[k], lengths[k]);
            total += found;
            checksum = (checksum * 31 + found) % 1000000007;
        }
    }
    printf("%lld rounds on %lld strings: %lld substrings in all, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)total, (long long)checksum);
    for (int64_t k = 0; k < count; k++) {
        free(strings[k]);
    }
    return 0;
}
