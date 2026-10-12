// Benchmark for #408: mirror of valid_word_abbreviation.kara (two
// pointers). Words and abbreviations are NUL-terminated buffers with
// their lengths kept beside them.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int valid_word_abbreviation(const unsigned char *w, int64_t wn, const unsigned char *a, int64_t an) {
    int64_t i = 0, j = 0;
    while (i < wn && j < an) {
        if (a[j] >= 48 && a[j] <= 57) {
            if (a[j] == 48) {
                return 0;
            }
            int64_t skip = 0;
            while (j < an && a[j] >= 48 && a[j] <= 57) {
                skip = skip * 10 + (a[j] - 48);
                j++;
            }
            i += skip;
        } else {
            if (w[i] != a[j]) {
                return 0;
            }
            i++;
            j++;
        }
    }
    return i == wn && j == an;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t count = argc > 1 ? atoll(argv[1]) : 20000;
    int64_t rounds = 1000, n = 20, seed = 408;
    unsigned char **words = malloc(count * sizeof *words);
    unsigned char **abbrs = malloc(count * sizeof *abbrs);
    int64_t *alen = malloc(count * sizeof *alen);
    for (int64_t t = 0; t < count; t++) {
        unsigned char *w = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) {
            w[i] = (unsigned char)(97 + step(&seed) % 2);
        }
        w[n] = 0;
        unsigned char *a = malloc(2 * n + 1);
        int64_t len = 0, i = 0;
        int number = 0;
        while (i < n) {
            if (number || step(&seed) % 2 == 0) {
                a[len++] = w[i];
                i++;
                number = 0;
            } else {
                int64_t run = 1 + step(&seed) % (n - i);
                len += sprintf((char *)a + len, "%lld", (long long)run);
                i += run;
                number = 1;
            }
        }
        a[len] = 0;
        words[t] = w;
        abbrs[t] = a;
        alen[t] = len;
    }
    int64_t valid = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t found = 0;
        for (int64_t i = 0; i < count; i++) {
            int64_t k = (i + r) % count;
            if (valid_word_abbreviation(words[i], n, abbrs[k], alen[k])) {
                found++;
            }
        }
        valid += found;
        checksum = (checksum * 31 + found) % 1000000007;
    }
    printf("%lld words, %lld rounds: %lld valid, checksum %lld\n", (long long)count, (long long)rounds, (long long)valid, (long long)checksum);
    for (int64_t t = 0; t < count; t++) {
        free(words[t]);
        free(abbrs[t]);
    }
    free(words);
    free(abbrs);
    free(alen);
    return 0;
}
