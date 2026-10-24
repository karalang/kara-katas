// LeetCode #936: Stamping The Sequence -- bench: stamps peeled off in
// reverse. Mirrors moves_to_stamp.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 936;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// writes the stamps into order and returns how many, or 0 if none
static int64_t moves_to_stamp(const char *s, int64_t m, const char *target, int64_t n, char *t,
                              int64_t *order) {
    memcpy(t, target, (size_t)n);
    int64_t erased = 0;
    int64_t len = 0;
    int progress = 1;
    while (progress && erased < n) {
        progress = 0;
        for (int64_t p = 0; p < n - m + 1; p++) {
            int fits = 1;
            int fresh = 0;
            for (int64_t k = 0; k < m; k++) {
                if (t[p + k] == s[k]) {
                    fresh = 1;
                } else if (t[p + k] != '?') {
                    fits = 0;
                }
            }
            if (fits && fresh) {
                for (int64_t k = 0; k < m; k++) {
                    if (t[p + k] != '?') {
                        t[p + k] = '?';
                        erased++;
                    }
                }
                order[len++] = p;
                progress = 1;
            }
        }
    }
    if (erased < n) {
        return 0;
    }
    for (int64_t i = 0, j = len - 1; i < j; i++, j--) {
        int64_t x = order[i];
        order[i] = order[j];
        order[j] = x;
    }
    return len;
}

int main(void) {
    const int64_t rounds = 100;
    const int64_t count = 50;
    const int64_t n = 1000;
    char *stamps[50];
    int64_t lens[50];
    char *targets[50];
    for (int64_t c = 0; c < count; c++) {
        int64_t m = 5 + next_random() % 16;
        char *s = malloc((size_t)m);
        for (int64_t k = 0; k < m; k++) {
            s[k] = (char)(97 + next_random() % 3);
        }
        char *out = malloc((size_t)n);
        memset(out, '?', (size_t)n);
        int64_t left = n;
        while (left > 0) {
            int64_t p = next_random() % (n - m + 1);
            for (int64_t k = 0; k < m; k++) {
                if (out[p + k] == '?') {
                    left--;
                }
                out[p + k] = s[k];
            }
        }
        if (c % 2 == 1) {
            int64_t at = next_random() % n;
            out[at] = (char)(97 + next_random() % 3);
        }
        stamps[c] = s;
        lens[c] = m;
        targets[c] = out;
    }
    char *t = malloc((size_t)n);
    int64_t *order = malloc((size_t)n * sizeof(int64_t));
    int64_t stamped = 0;
    int64_t turns = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t c = (r + i) % count;
            int64_t len = moves_to_stamp(stamps[c], lens[c], targets[c], n, t, order);
            if (len > 0) {
                stamped++;
            }
            turns += len;
            for (int64_t k = 0; k < len; k++) {
                check = (check * 1000003 + order[k] + 1) % 1000000007;
            }
        }
    }
    printf("%lld rounds over %lld targets of %lld letters: %lld stamped, %lld stamps, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)stamped, (long long)turns,
           (long long)check);
    return 0;
}
