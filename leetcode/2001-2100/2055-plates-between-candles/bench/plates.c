// LeetCode #2055: Plates Between Candles -- C mirror of the ★ arm's
// benchmark (plates.kara): the same 50 strings and five million queries,
// the same plate counts and nearest candles. C reads the string's bytes in
// place, where the Kāra, Rust and Go programs first collect its characters.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2055;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

#define N 100000

static void plates_between_candles(const char *s, int64_t n, const int64_t *ql, const int64_t *qr,
                                   int64_t q, int64_t *answers) {
    int64_t *plates = malloc((n + 1) * sizeof(int64_t));
    int64_t *before = malloc(n * sizeof(int64_t));
    int64_t *after = malloc(n * sizeof(int64_t));
    plates[0] = 0;
    int64_t last = -1;
    for (int64_t i = 0; i < n; i++) {
        plates[i + 1] = plates[i] + (s[i] == '*' ? 1 : 0);
        if (s[i] == '|') last = i;
        before[i] = last;
    }
    int64_t next = n;
    for (int64_t i = n - 1; i >= 0; i--) {
        if (s[i] == '|') next = i;
        after[i] = next;
    }
    for (int64_t k = 0; k < q; k++) {
        int64_t first = after[ql[k]], lst = before[qr[k]];
        answers[k] = first < lst ? plates[lst] - plates[first] : 0;
    }
    free(plates);
    free(before);
    free(after);
}

int main(void) {
    char *s = malloc(N + 1);
    int64_t *ql = malloc(N * sizeof(int64_t)), *qr = malloc(N * sizeof(int64_t));
    int64_t *answers = malloc(N * sizeof(int64_t));
    int64_t total = 0, check = 0;
    for (int64_t t = 0; t < 50; t++) {
        int64_t every = t + 1;
        for (int i = 0; i < N; i++) s[i] = next_random() % every == 0 ? '|' : '*';
        s[N] = 0;
        for (int i = 0; i < N; i++) {
            int64_t a = wide() % N;
            int64_t b = wide() % N;
            ql[i] = a < b ? a : b;
            qr[i] = a < b ? b : a;
        }
        plates_between_candles(s, N, ql, qr, N, answers);
        for (int i = 0; i < N; i++) {
            total += answers[i];
            check = (check * 31 + answers[i] + 1) % 1000000007;
        }
    }
    printf("50 strings: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(s);
    free(ql);
    free(qr);
    free(answers);
    return 0;
}
