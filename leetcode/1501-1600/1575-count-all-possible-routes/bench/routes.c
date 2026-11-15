// LeetCode #1575: Count All Possible Routes -- bench: the ★ arm (routes to
// the finish filled from no fuel up) over 100 problems of 60 distinct
// locations below 300 and a fuel of 200, every problem drawn first.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 60
#define FUEL 200

static int64_t count_routes(const int64_t *locations, int64_t n, int64_t start, int64_t finish, int64_t fuel) {
    const int64_t m = 1000000007;
    int64_t **ways = malloc(sizeof(int64_t *) * (fuel + 1));
    for (int64_t f = 0; f < fuel + 1; f++) {
        ways[f] = calloc(n, sizeof(int64_t));
    }
    for (int64_t f = 0; f < fuel + 1; f++) {
        for (int64_t c = 0; c < n; c++) {
            int64_t total = c == finish ? 1 : 0;
            for (int64_t d = 0; d < n; d++) {
                int64_t cost = llabs(locations[c] - locations[d]);
                if (d != c && cost <= f) {
                    total = (total + ways[f - cost][d]) % m;
                }
            }
            ways[f][c] = total;
        }
    }
    int64_t answer = ways[fuel][start];
    for (int64_t f = 0; f < fuel + 1; f++) {
        free(ways[f]);
    }
    free(ways);
    return answer;
}

static int64_t seed = 1575;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    static int64_t locations[100][N];
    int64_t starts[100], finishes[100];
    for (int p = 0; p < 100; p++) {
        int64_t len = 0;
        while (len < N) {
            int64_t x = next_random() % 300;
            int seen = 0;
            for (int64_t i = 0; i < len; i++) {
                if (locations[p][i] == x) {
                    seen = 1;
                    break;
                }
            }
            if (!seen) {
                locations[p][len++] = x;
            }
        }
        starts[p] = next_random() % N;
        finishes[p] = next_random() % N;
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < 100; p++) {
        int64_t routes = count_routes(locations[p], N, starts[p], finishes[p], FUEL);
        total += routes;
        check = mix(check, routes);
    }
    printf("100 problems of %d locations and fuel 200: routes total %lld, checksum %lld\n", N, (long long)total,
           (long long)check);
    return 0;
}
