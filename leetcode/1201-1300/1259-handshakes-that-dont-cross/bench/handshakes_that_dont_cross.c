// LeetCode #1259 bench, in C: the ★ arm (ways[k] for k pairs, summed over
// where person 0's partner sits, modulo 10^9 + 7) for every even count of
// people from 2 to 1000, 4 rounds; each count folded into a checksum.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t number_of_ways(int64_t num_people) {
    const int64_t m = 1000000007;
    int64_t pairs = num_people / 2;
    int64_t *ways = calloc(pairs + 1, sizeof(int64_t));
    ways[0] = 1;
    for (int64_t k = 1; k <= pairs; k++)
        for (int64_t left = 0; left < k; left++)
            ways[k] = (ways[k] + ways[left] * ways[k - 1 - left]) % m;
    int64_t r = ways[pairs];
    free(ways);
    return r;
}

int main(void) {
    int64_t check = 0;
    for (int r = 0; r < 4; r++)
        for (int64_t n = 2; n <= 1000; n += 2)
            check = (check * 131 + number_of_ways(n)) % 1000000007;
    printf("4 rounds of 2 to 1000 people: checksum %lld\n", (long long)check);
    return 0;
}
