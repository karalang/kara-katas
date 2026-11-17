// LeetCode #1184: Distance Between Bus Stops -- the ★ arm in C: the arc
// from the lower stop to the higher, against the whole ring less it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t distance_between_bus_stops(const int64_t *distance, int n, int64_t start, int64_t destination) {
    int64_t from = start < destination ? start : destination;
    int64_t to = start < destination ? destination : start;
    int64_t total = 0, one_way = 0;
    for (int i = 0; i < n; i++) total += distance[i];
    for (int64_t i = from; i < to; i++) one_way += distance[i];
    return one_way < total - one_way ? one_way : total - one_way;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

enum { RINGS = 50, N = 10000, PAIRS = 200 };
static int64_t rings[RINGS][N];
static int64_t pairs[RINGS * PAIRS][2];

int main(void) {
    int64_t seed = 1184;
    for (int r = 0; r < RINGS; r++) {
        for (int i = 0; i < N; i++) rings[r][i] = next_random(&seed) % 10001;
        for (int k = 0; k < PAIRS; k++) {
            int64_t start = next_random(&seed) % 10000;
            int64_t destination = next_random(&seed) % 10000;
            pairs[r * PAIRS + k][0] = start;
            pairs[r * PAIRS + k][1] = destination;
        }
    }
    int rounds = 10;
    int64_t check = 0;
    for (int round = 0; round < rounds; round++)
        for (int r = 0; r < RINGS; r++)
            for (int k = 0; k < PAIRS; k++)
                check = (check * 131 + distance_between_bus_stops(rings[r], N, pairs[r * PAIRS + k][0], pairs[r * PAIRS + k][1]) + round) % 1000000007;
    printf("%d rounds of 10000 queries over 50 rings: checksum %lld\n", rounds, (long long)check);
    return 0;
}
