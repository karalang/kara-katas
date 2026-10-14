// Benchmark for #564: C mirror of the ★ arm (five candidates); see
// nearest_palindromic.kara. Each mirrored candidate is written into a
// `malloc`'d string and read back with `strtoll`, and the answer is a
// fresh `malloc`'d string, as the Kāra arm's are fresh `String`s.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t pow10i(int64_t e) {
    int64_t r = 1;
    for (int64_t i = 0; i < e; i++) r *= 10;
    return r;
}

static char *to_text(int64_t x) {
    char *s = malloc(24);
    snprintf(s, 24, "%lld", (long long)x);
    return s;
}

static int64_t mirrored(int64_t half, int64_t length) {
    char *text = to_text(half);
    int64_t len = (int64_t)strlen(text);
    char *s = malloc(48);
    memcpy(s, text, len);
    int64_t at = len;
    int64_t i = (length / 2 < len ? length / 2 : len) - 1;
    while (i >= 0) {
        s[at++] = text[i];
        i -= 1;
    }
    s[at] = 0;
    int64_t r = strtoll(s, NULL, 10);
    free(s);
    free(text);
    return r;
}

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static char *nearest_palindromic(const char *n) {
    int64_t value = strtoll(n, NULL, 10);
    int64_t length = (int64_t)strlen(n);
    char front[24];
    int64_t hl = (length + 1) / 2;
    memcpy(front, n, hl);
    front[hl] = 0;
    int64_t half = strtoll(front, NULL, 10);
    int64_t candidates[5] = {pow10i(length - 1) - 1, pow10i(length) + 1, 0, 0, 0};
    for (int64_t k = 0; k < 3; k++) candidates[2 + k] = mirrored(half - 1 + k, length);
    int64_t best = -1;
    for (int k = 0; k < 5; k++) {
        int64_t c = candidates[k];
        if (c == value || c < 0) continue;
        int64_t d = abs64(c - value);
        int64_t bd = abs64(best - value);
        if (best == -1 || d < bd || (d == bd && c < best)) best = c;
    }
    return to_text(best);
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *random_number(int64_t t, int64_t *seed) {
    int64_t length = 1 + step(seed) % 18;
    int64_t digits[18];
    digits[0] = 1 + step(seed) % 9;
    for (int64_t i = 1; i < length; i++) digits[i] = step(seed) % 10;
    if (t % 3 == 1) {
        for (int64_t i = 0; i < length / 2; i++) digits[length - 1 - i] = digits[i];
    }
    int64_t value = 0;
    for (int64_t i = 0; i < length; i++) value = value * 10 + digits[i];
    if (t % 3 == 2) {
        value = pow10i(length - 1) + step(seed) % 7 - 3;
        if (value < 1) value = 1;
    }
    return to_text(value);
}

int main(void) {
    int64_t count = 10000;
    int64_t rounds = 300;
    int64_t seed = 564;
    char **numbers = malloc(count * sizeof(char *));
    for (int64_t t = 0; t < count; t++) numbers[t] = random_number(t, &seed);
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            char *text = nearest_palindromic(numbers[(round * 7 + g) % count]);
            int64_t got = strtoll(text, NULL, 10);
            free(text);
            checksum = (checksum * 31 + got % 1000000007) % 1000000007;
        }
    }
    printf("%lld numbers, %lld rounds: checksum %lld\n", (long long)count, (long long)rounds,
           (long long)checksum);
    for (int64_t t = 0; t < count; t++) free(numbers[t]);
    free(numbers);
    return 0;
}
