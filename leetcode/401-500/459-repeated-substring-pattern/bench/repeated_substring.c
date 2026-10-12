// Benchmark for #459: mirror of repeated_substring.kara (the ★ arm, every
// proper divisor) on the same workload.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool repeated_substring_pattern(const char *s, int64_t n) {
    char *cs = malloc(n);
    memcpy(cs, s, n);
    bool result = false;
    for (int64_t d = 1; d < n / 2 + 1 && !result; d++) {
        if (n % d != 0) {
            continue;
        }
        bool repeats = true;
        for (int64_t i = d; i < n; i++) {
            if (cs[i] != cs[i - d]) {
                repeats = false;
                break;
            }
        }
        if (repeats) {
            result = true;
        }
    }
    free(cs);
    return result;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t strings = 10;
    const int64_t n = 100000;
    const int64_t rounds = 40;
    const int64_t units[10] = {1, 5, 32, 100, 625, 1000, 3125, 5000, 20000, 50000};
    int64_t seed = 459;
    char *all[10];
    char *original = malloc(n);
    for (int64_t a = 0; a < strings; a++) {
        char *unit = malloc(units[a]);
        for (int64_t i = 0; i < units[a]; i++) {
            unit[i] = (char)(97 + next_random(&seed) % 26);
        }
        all[a] = malloc(n);
        for (int64_t i = 0; i < n; i++) {
            all[a][i] = unit[i % units[a]];
        }
        free(unit);
    }
    int64_t found = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t a = 0; a < strings; a++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            int64_t k = n / 2 + (hi * 65536 + lo) % (n / 2);
            bool punch = next_random(&seed) % 2 == 0;
            memcpy(original, all[a], n);
            if (punch) {
                all[a][k] = (char)(97 + (all[a][k] - 97 + 1) % 26);
            }
            bool has = repeated_substring_pattern(all[a], n);
            memcpy(all[a], original, n);
            if (has) {
                found += 1;
            }
            checksum = (checksum * 31 + (has ? units[a] : k)) % 1000000007;
        }
    }
    printf("%lld rounds on %lld strings of %lld: %lld repeat a substring, checksum %lld\n",
           (long long)rounds, (long long)strings, (long long)n, (long long)found, (long long)checksum);
    for (int64_t a = 0; a < strings; a++) {
        free(all[a]);
    }
    free(original);
    return 0;
}
