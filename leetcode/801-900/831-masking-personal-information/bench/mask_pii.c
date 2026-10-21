// Benchmark for #831: Masking Personal Information -- the ★ arm (by the rules).
//
// Mirrors mask_pii.kara: an email keeps its name's first and last letter,
// lowered, around five `*`, and its domain lowered; a phone number shows
// its last four digits and masks the country code, the digits before the
// last ten. As in the Kāra program, the lowered copy, the digits and the
// result are each a fresh allocation.

#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *mask_pii(const char *s, int64_t len) {
    const char *at = memchr(s, '@', (size_t)len);
    if (at) {
        int64_t a = at - s;
        char *lower = malloc((size_t)len + 1);
        for (int64_t i = 0; i < len; i++) lower[i] = (char)tolower((unsigned char)s[i]);
        lower[len] = 0;
        int64_t tail = len - (a - 1);
        char *out = malloc((size_t)(6 + tail + 1));
        out[0] = lower[0];
        memcpy(out + 1, "*****", 5);
        memcpy(out + 6, lower + a - 1, (size_t)tail);
        out[6 + tail] = 0;
        free(lower);
        return out;
    }
    char *digits = malloc((size_t)len + 1);
    int64_t n = 0;
    for (int64_t i = 0; i < len; i++)
        if (isdigit((unsigned char)s[i])) digits[n++] = s[i];
    char *out = malloc(32);
    int64_t k = 0;
    if (n > 10) {
        out[k++] = '+';
        for (int64_t i = 0; i < n - 10; i++) out[k++] = '*';
        out[k++] = '-';
    }
    memcpy(out + k, "***-***-", 8);
    k += 8;
    memcpy(out + k, digits + n - 4, 4);
    k += 4;
    out[k] = 0;
    free(digits);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char letter(int64_t *seed) {
    int64_t r = next_random(seed) % 52;
    return r < 26 ? (char)('a' + r) : (char)('A' + r - 26);
}

int main(void) {
    const int64_t count = 64, rounds = 12000000;
    const char separators[5] = {'+', '-', '(', ')', ' '};
    int64_t seed = 831;
    char *strings[64];
    int64_t lens[64];
    for (int64_t g = 0; g < count; g++) {
        char buf[64];
        int64_t k = 0;
        if (g % 2 == 0) {
            int64_t m = 2 + next_random(&seed) % 19;
            for (int64_t i = 0; i < m; i++) buf[k++] = letter(&seed);
            buf[k++] = '@';
            m = 1 + next_random(&seed) % 8;
            for (int64_t i = 0; i < m; i++) buf[k++] = letter(&seed);
            buf[k++] = '.';
            m = 1 + next_random(&seed) % 8;
            for (int64_t i = 0; i < m; i++) buf[k++] = letter(&seed);
        } else {
            int64_t m = 10 + next_random(&seed) % 4;
            for (int64_t i = 0; i < m; i++) {
                if (next_random(&seed) % 3 == 0) buf[k++] = separators[next_random(&seed) % 5];
                buf[k++] = (char)('0' + next_random(&seed) % 10);
            }
        }
        strings[g] = malloc((size_t)k + 1);
        memcpy(strings[g], buf, (size_t)k);
        strings[g][k] = 0;
        lens[g] = k;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        char *m = mask_pii(strings[round % count], lens[round % count]);
        int64_t len = (int64_t)strlen(m);
        total += len;
        checksum = (checksum * 131 + (unsigned char)m[len - 1]) % 1000000007;
        free(m);
    }
    printf("%lld rounds of %lld strings: %lld characters, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) free(strings[g]);
    return 0;
}
