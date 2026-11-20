// LeetCode #1269 bench, in C: the ★ arm (the ways to stand on each of
// the first `steps / 2 + 1` cells, a new row per step) on 1000 random cases
// of 1 to 500 steps in 1 to 400 cells or a million, drawn once, 20 rounds;
// every answer folded into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007

static int64_t num_ways(int64_t steps, int64_t arr_len) {
    int64_t width = arr_len < steps / 2 + 1 ? arr_len : steps / 2 + 1;
    int64_t *ways = calloc(width, sizeof(int64_t));
    ways[0] = 1;
    for (int64_t s = 0; s < steps; s++) {
        int64_t *next = calloc(width, sizeof(int64_t));
        for (int64_t i = 0; i < width; i++) {
            int64_t w = ways[i];
            if (i > 0) w += ways[i - 1];
            if (i + 1 < width) w += ways[i + 1];
            next[i] = w % MOD;
        }
        free(ways);
        ways = next;
    }
    int64_t answer = ways[0];
    free(ways);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1269;
    int64_t steps[1000], lens[1000];
    for (int c = 0; c < 1000; c++) {
        steps[c] = next_random(&seed) % 500 + 1;
        lens[c] = c % 4 == 0 ? 1000000 : next_random(&seed) % 400 + 1;
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 20; round++)
        for (int c = 0; c < 1000; c++)
            check = (check * 131 + num_ways(steps[c], lens[c]) + round) % 1000000007;
    printf("20 rounds of 1000 cases: checksum %lld\n", (long long)check);
    return 0;
}
