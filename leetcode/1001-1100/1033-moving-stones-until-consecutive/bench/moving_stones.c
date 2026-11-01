// LeetCode #1033: Moving Stones Until Consecutive -- bench
// Mirrors ./moving_stones.kara; see ../README.md § Benchmarks. The three
// stones and the two answers live in small arrays on the stack, where the
// Kāra, Rust and Go versions build two short vectors per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int cmp_i64(const void *p, const void *q) {
    int64_t a = *(const int64_t *)p, b = *(const int64_t *)q;
    return (a > b) - (a < b);
}

static void num_moves_stones(int64_t a, int64_t b, int64_t c, int64_t out[2]) {
    int64_t s[3] = {a, b, c};
    qsort(s, 3, sizeof s[0], cmp_i64);
    int64_t x = s[0], y = s[1], z = s[2];
    int64_t fewest = z - x == 2 ? 0 : (y - x <= 2 || z - y <= 2) ? 1 : 2;
    out[0] = fewest;
    out[1] = z - x - 2;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 1000000;
    const int64_t rounds = 40;
    int64_t seed = 1033;
    int64_t (*cases)[3] = malloc(sizeof(int64_t[3]) * count);
    int64_t n = 0;
    while (n < count) {
        int64_t a = next_random(&seed) % 100 + 1;
        int64_t b = next_random(&seed) % 100 + 1;
        int64_t c = next_random(&seed) % 100 + 1;
        if (a != b && b != c && a != c) {
            cases[n][0] = a;
            cases[n][1] = b;
            cases[n][2] = c;
            n++;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t moves[2];
            num_moves_stones(cases[i][0], cases[i][1], cases[i][2], moves);
            total += moves[0] + moves[1];
            check = (check * 131 + moves[0] * 101 + moves[1]) % 1000000007;
        }
    }
    printf("%lld triples, %lld rounds: sum %lld, checksum %lld\n", (long long)count, (long long)rounds, (long long)total, (long long)check);
    free(cases);
    return 0;
}
