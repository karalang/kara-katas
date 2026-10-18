// LeetCode #709: To Lower Case -- character by character.
// Benchmark mirror of the Kara star arm: copy each character into a new
// string, moving 'A' to 'Z' up by 32.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *to_lower_case(const char *s, int64_t n) {
    char *out = malloc(n + 1);
    for (int64_t i = 0; i < n; i++) {
        char c = s[i];
        out[i] = (c >= 'A' && c <= 'Z') ? (char)(c + 32) : c;
    }
    out[n] = 0;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 709;
    enum { COUNT = 10000, LEN = 100 };
    char **strings = malloc(COUNT * sizeof(char *));
    for (int i = 0; i < COUNT; i++) {
        strings[i] = malloc(LEN + 1);
        for (int j = 0; j < LEN; j++) {
            strings[i][j] = (char)(32 + next_random(&seed) % 95);
        }
        strings[i][LEN] = 0;
    }
    char **results = malloc(COUNT * sizeof(char *));
    for (int i = 0; i < COUNT; i++) {
        results[i] = malloc(LEN + 1);
        memcpy(results[i], strings[i], LEN + 1);
    }
    int64_t sum = 0;
    for (int round = 0; round < 50; round++) {
        for (int i = 0; i < COUNT; i++) {
            free(results[i]);
            results[i] = to_lower_case(strings[i], LEN);
            sum += (unsigned char)results[i][(round + i) % LEN];
        }
    }
    for (int i = 0; i < COUNT; i++) {
        for (int j = 0; j < LEN; j++) {
            sum += (unsigned char)results[i][j];
        }
        free(results[i]);
    }
    free(results);
    for (int i = 0; i < COUNT; i++) {
        free(strings[i]);
    }
    free(strings);
    printf("50 rounds of 10000 strings of 100 characters: sum %lld\n", (long long)sum);
    return 0;
}
