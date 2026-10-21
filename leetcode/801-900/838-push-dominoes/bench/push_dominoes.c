// Benchmark for #838: Push Dominoes -- the ★ arm (the stretches between pushes).
//
// Mirrors push_dominoes.kara: the walk goes from push to push, with an L
// imagined before the line and an R after it. Between two pushes the same
// way every domino falls that way; between an R and an L the two halves
// fall inward. As in the Kāra program, the line is copied out to be
// worked on and the answer built one domino at a time, growing by
// doubling.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    int64_t len, cap;
} Str;

static void push(Str *s, char c) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 8;
        s->data = realloc(s->data, (size_t)s->cap);
    }
    s->data[s->len++] = c;
}

static Str push_dominoes(const char *dominoes, int64_t n) {
    char *d = malloc((size_t)n);
    memcpy(d, dominoes, (size_t)n);
    int64_t left = -1;
    char left_push = 'L';
    for (int64_t right = 0; right < n + 1; right++) {
        char right_push = right == n ? 'R' : d[right];
        if (right_push == '.') continue;
        if (left_push == right_push) {
            for (int64_t i = left + 1; i < right; i++) d[i] = right_push;
        } else if (left_push == 'R') {
            int64_t i = left + 1, j = right - 1;
            while (i < j) {
                d[i] = 'R';
                d[j] = 'L';
                i += 1;
                j -= 1;
            }
        }
        left = right;
        left_push = right_push;
    }
    Str out = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) push(&out, d[i]);
    free(d);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 16 lines drawn once, each of LeetCode's longest, 10^5 dominoes,
    // line g pushing each domino left with chance 1 + 4g in 200 and right
    // with the same chance. Each round settles the next line and reads 16
    // dominoes of the result.
    enum { COUNT = 16, N = 100000 };
    const int64_t rounds = 1300, n = N;
    int64_t seed = 838;
    static char lines[COUNT][N];
    for (int64_t g = 0; g < COUNT; g++) {
        int64_t pushed = 1 + 4 * g;
        for (int64_t i = 0; i < n; i++) {
            int64_t r = next_random(&seed) % 200;
            lines[g][i] = r < pushed ? 'L' : r < 2 * pushed ? 'R' : '.';
        }
    }
    int64_t fallen = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        Str out = push_dominoes(lines[round % COUNT], n);
        for (int64_t t = 0; t < 16; t++) {
            int64_t b = (unsigned char)out.data[(round * 7919 + t * 6151) % n];
            if (b != 46) fallen += 1;
            checksum = (checksum * 31 + b) % 1000000007;
        }
        free(out.data);
    }
    printf("%lld rounds of %d lines: %lld of the dominoes read fallen, checksum %lld\n", (long long)rounds, COUNT,
           (long long)fallen, (long long)checksum);
    return 0;
}
