// Benchmark for #411: mirror of min_abbreviation.kara (masks over the
// letters).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t mask_length(int64_t m, int64_t mask) {
    int64_t length = 0;
    int in_run = 0;
    for (int64_t i = 0; i < m; i++) {
        if ((mask >> i) & 1) {
            length++;
            in_run = 0;
        } else if (!in_run) {
            length++;
            in_run = 1;
        }
    }
    return length;
}

/* Writes the abbreviation into out (NUL-terminated) and returns its byte length. */
static int64_t abbreviate(const char *t, int64_t m, int64_t mask, char *out) {
    int64_t len = 0, run = 0;
    for (int64_t i = 0; i < m; i++) {
        if ((mask >> i) & 1) {
            if (run > 0) {
                len += sprintf(out + len, "%lld", (long long)run);
                run = 0;
            }
            out[len++] = t[i];
        } else {
            run++;
        }
    }
    if (run > 0) {
        len += sprintf(out + len, "%lld", (long long)run);
    }
    out[len] = 0;
    return len;
}

static int64_t min_abbreviation(const char *t, int64_t m, char **dict, int64_t n, char *out) {
    int64_t *diffs = malloc((n + 1) * sizeof *diffs);
    int64_t nd = 0;
    for (int64_t d = 0; d < n; d++) {
        if ((int64_t)strlen(dict[d]) == m) {
            int64_t diff = 0;
            for (int64_t i = 0; i < m; i++) {
                if (dict[d][i] != t[i]) {
                    diff |= (int64_t)1 << i;
                }
            }
            diffs[nd++] = diff;
        }
    }
    int64_t best_mask = ((int64_t)1 << m) - 1, best_length = m;
    for (int64_t mask = 0; mask < ((int64_t)1 << m); mask++) {
        int64_t length = mask_length(m, mask);
        if (length < best_length) {
            int unique = 1;
            for (int64_t d = 0; d < nd; d++) {
                if ((mask & diffs[d]) == 0) {
                    unique = 0;
                    break;
                }
            }
            if (unique) {
                best_length = length;
                best_mask = mask;
            }
        }
    }
    free(diffs);
    return abbreviate(t, m, best_mask, out);
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t targets = argc > 1 ? atoll(argv[1]) : 30;
    int64_t m = 20, words = 2, seed = 411, total = 0, checksum = 0;
    char target[32], out[64];
    char **dict = malloc(words * sizeof *dict);
    for (int64_t w = 0; w < words; w++) {
        dict[w] = malloc(m + 1);
    }
    for (int64_t t = 0; t < targets; t++) {
        for (int64_t i = 0; i < m; i++) {
            target[i] = (char)(97 + step(&seed) % 2);
        }
        target[m] = 0;
        int64_t n = 0;
        while (n < words) {
            for (int64_t i = 0; i < m; i++) {
                dict[n][i] = (char)(97 + step(&seed) % 2);
            }
            dict[n][m] = 0;
            if (strcmp(dict[n], target) != 0) {
                n++;
            }
        }
        int64_t len = min_abbreviation(target, m, dict, n, out);
        total += len;
        for (int64_t i = 0; i < len; i++) {
            checksum = (checksum * 31 + (unsigned char)out[i]) % 1000000007;
        }
    }
    printf("%lld targets of %lld letters, %lld words each: total %lld, checksum %lld\n", (long long)targets, (long long)m, (long long)words, (long long)total, (long long)checksum);
    for (int64_t w = 0; w < words; w++) {
        free(dict[w]);
    }
    free(dict);
    return 0;
}
