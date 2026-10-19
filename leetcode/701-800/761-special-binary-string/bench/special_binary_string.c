// LeetCode 761 — Special Binary String: benchmark, the ★ arm in C.
// 200,000 random special strings of 50 characters.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int descending(const void *a, const void *b) {
    return strcmp(*(char *const *)b, *(char *const *)a);
}

// The largest form of s[0..n), as a new string.
static char *make_largest_special(const char *s, int n) {
    char **mountains = malloc((size_t)(n / 2 + 1) * sizeof(char *));
    int count = 0, depth = 0, start = 0;
    for (int i = 0; i < n; i++) {
        depth += s[i] == '1' ? 1 : -1;
        if (depth == 0) {
            char *inside = make_largest_special(s + start + 1, i - start - 1);
            char *m = malloc((size_t)(i - start + 2));
            m[0] = '1';
            memcpy(m + 1, inside, (size_t)(i - start - 1));
            m[i - start] = '0';
            m[i - start + 1] = '\0';
            free(inside);
            mountains[count++] = m;
            start = i + 1;
        }
    }
    qsort(mountains, (size_t)count, sizeof(char *), descending);
    char *out = malloc((size_t)n + 1);
    int at = 0;
    for (int k = 0; k < count; k++) {
        size_t len = strlen(mountains[k]);
        memcpy(out + at, mountains[k], len);
        at += (int)len;
        free(mountains[k]);
    }
    out[at] = '\0';
    free(mountains);
    return out;
}

static int64_t seed = 761;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 200000;
    int64_t leading = 0, check = 0;
    char s[51];
    for (int r = 0; r < rounds; r++) {
        int ones = 0, depth = 0;
        for (int i = 0; i < 50; i++) {
            if (ones < 25 && (depth == 0 || next_random() % 2 == 0)) {
                s[i] = '1';
                ones++;
                depth++;
            } else {
                s[i] = '0';
                depth--;
            }
        }
        s[50] = '\0';
        char *largest = make_largest_special(s, 50);
        int lead = 1;
        for (int i = 0; i < 50; i++) {
            if (largest[i] == '0') lead = 0;
            if (lead) leading++;
            check = (check * 2 + (largest[i] == '1')) % 1000000007;
        }
        free(largest);
    }
    printf("%d strings of 50 characters: %lld leading 1s, checksum %lld\n", rounds, (long long)leading, (long long)check);
    return 0;
}
