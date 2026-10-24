// Benchmark: LeetCode #942 DI String Match -- the ★ arm, the smallest
// and largest left, on 20 strings of 100000 letters, LeetCode's longest,
// in 50 rounds. Mirrors di_string_match.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t *di_string_match(const char *s, int64_t n) {
    int64_t *perm = malloc(sizeof(int64_t) * (n + 1));
    int64_t lo = 0, hi = n;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == 'I') {
            perm[i] = lo++;
        } else {
            perm[i] = hi--;
        }
    }
    perm[n] = lo;
    return perm;
}

static int64_t seed = 942;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char strings[20][N + 1];

int main(void) {
    int rounds = 50, count = 20;
    for (int w = 0; w < count; w++) {
        int64_t odds = 1 + next_random() % 15;
        for (int i = 0; i < N; i++) strings[w][i] = next_random() % 16 < odds ? 'I' : 'D';
        strings[w][N] = 0;
    }
    int64_t check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            int64_t *perm = di_string_match(strings[(r + i) % count], N);
            check = (check * 1000003 + perm[0] * 3 + perm[N / 2] * 5 + perm[N] * 7) % 1000000007;
            free(perm);
        }
    }
    printf("%d rounds over %d strings of %d letters: checksum %lld\n", rounds, count, N, (long long)check);
    return 0;
}
