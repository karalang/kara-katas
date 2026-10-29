// LeetCode #1023: Camelcase Matching -- bench
// Mirrors ./camel_match.kara; see ../README.md § Benchmarks.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char *data;
    int64_t len;
} Str;

static bool *camel_match(const Str *queries, int64_t count, const Str *pattern) {
    bool *answers = malloc(count * sizeof *answers);
    for (int64_t k = 0; k < count; k++) {
        int64_t i = 0;
        bool ok = true;
        for (int64_t j = 0; j < queries[k].len; j++) {
            char c = queries[k].data[j];
            if (i < pattern->len && c == pattern->data[i]) {
                i += 1;
            } else if (c >= 'A' && c <= 'Z') {
                ok = false;
                break;
            }
        }
        answers[k] = ok && i == pattern->len;
    }
    return answers;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char random_letter(int64_t *seed, int64_t capitals) {
    int upper = next_random(seed) % 8 < capitals;
    int64_t k = next_random(seed) % 26;
    return (char)((upper ? 65 : 97) + k);
}

int main(void) {
    const int64_t count = 500, rounds = 150, per = 100;
    int64_t seed = 1023, letters = 0;
    Str *patterns = malloc(count * sizeof *patterns);
    Str *queries = malloc(count * per * sizeof *queries);
    for (int64_t g = 0; g < count; g++) {
        int64_t plen = 1 + next_random(&seed) % 100;
        patterns[g].data = malloc(plen);
        patterns[g].len = plen;
        for (int64_t i = 0; i < plen; i++) patterns[g].data[i] = random_letter(&seed, 2);
        for (int64_t k = 0; k < per; k++) {
            Str *q = &queries[g * per + k];
            q->data = malloc(100);
            q->len = 0;
            if (k % 2 == 0) {
                int64_t left = next_random(&seed) % (100 - plen + 1);
                int64_t at = 0;
                while (at < plen || left > 0) {
                    if (left > 0 && (at == plen || next_random(&seed) % 2 == 0)) {
                        q->data[q->len++] = random_letter(&seed, 1);
                        left -= 1;
                    } else {
                        q->data[q->len++] = patterns[g].data[at++];
                    }
                }
            } else {
                int64_t n = 1 + next_random(&seed) % 100;
                for (int64_t i = 0; i < n; i++) q->data[q->len++] = random_letter(&seed, 2);
            }
            letters += q->len;
        }
    }
    int64_t matched = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t g = 0; g < count; g++) {
            bool *answers = camel_match(&queries[g * per], per, &patterns[g]);
            for (int64_t k = 0; k < per; k++) {
                if (answers[k]) {
                    matched += 1;
                    check = (check * 31 + k + 1) % 1000000007;
                }
            }
            free(answers);
        }
    }
    printf("%lld cases, %lld query letters, %lld rounds: %lld match, checksum %lld\n", (long long)count,
           (long long)letters, (long long)rounds, (long long)matched, (long long)check);
    return 0;
}
