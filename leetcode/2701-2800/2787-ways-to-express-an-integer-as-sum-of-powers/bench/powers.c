// LeetCode #2787: Ways to Express an Integer as Sum of Powers -- the bench
// in C: the ★ arm over every n from 1 to 300 with every x from 1 to 5, 20
// times over.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t ipow(int64_t b, int64_t e) {
    int64_t r = 1;
    while (e-- > 0) r *= b;
    return r;
}

static int64_t number_of_ways(int64_t n, int64_t x) {
    const int64_t modulus = 1000000007;
    int64_t *ways = calloc(n + 1, sizeof(int64_t));
    ways[0] = 1;
    for (int64_t i = 1; ipow(i, x) <= n; i++) {
        int64_t p = ipow(i, x);
        for (int64_t s = n; s >= p; s--) ways[s] = (ways[s] + ways[s - p]) % modulus;
    }
    int64_t w = ways[n];
    free(ways);
    return w;
}

int main(void) {
    int rounds = 20;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int64_t n = 1; n <= 300; n++)
            for (int64_t x = 1; x <= 5; x++) {
                int64_t w = number_of_ways(n, x);
                total += w;
                check = (check * 31 + w + r) % 1000000007;
            }
    printf("1500 pairs, %d rounds: ways sum to %lld, checksum %lld\n", rounds, (long long)total, (long long)check);
    return 0;
}
