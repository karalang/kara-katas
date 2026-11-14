// LeetCode #1556: Thousand Separator -- bench: the ★ arm (a dot before
// every digit whose distance from the end is a positive multiple of three)
// over 1000000 numbers below 2^31, each with its own count of 1 to 10
// digits, drawn once, each asked 3 times. C mirror of separator.kara:
// the digits by snprintf, the result a fresh heap string per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *thousand_separator(int64_t n) {
    char digits[24];
    int length = snprintf(digits, sizeof digits, "%lld", (long long)n);
    char *out = malloc(length + length / 3 + 1);
    int k = 0;
    for (int i = 0; i < length; i++) {
        if (i > 0 && (length - i) % 3 == 0) out[k++] = '.';
        out[k++] = digits[i];
    }
    out[k] = 0;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1556;
    static int64_t numbers[1000000];
    for (int i = 0; i < 1000000; i++) {
        int64_t digits = next_random(&seed) % 10 + 1;
        int64_t top = 1;
        for (int64_t d = 0; d < digits; d++) top *= 10;
        int64_t wide = (next_random(&seed) * 32768 + next_random(&seed)) * 32768 + next_random(&seed);
        int64_t n = wide % top;
        numbers[i] = n < 2147483647 ? n : 2147483647;
    }
    int64_t check = 0, length = 0;
    for (int pass = 0; pass < 3; pass++) {
        for (int i = 0; i < 1000000; i++) {
            char *text = thousand_separator(numbers[i]);
            for (char *p = text; *p; p++) {
                check = (check * 31 + (unsigned char)*p + 1) % 1000000007;
                length++;
            }
            free(text);
        }
    }
    printf("3 passes over 1000000 numbers: %lld characters, checksum %lld\n", (long long)length,
           (long long)check);
    return 0;
}
