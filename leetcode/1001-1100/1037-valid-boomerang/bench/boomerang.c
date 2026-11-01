// LeetCode #1037: Valid Boomerang -- bench
// Mirrors ../boomerang.kara; see ../README.md § Benchmarks.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct { int64_t x, y; } Point;

static bool is_boomerang(const Point *p) {
    return (p[1].x - p[0].x) * (p[2].y - p[0].y) - (p[1].y - p[0].y) * (p[2].x - p[0].x) != 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 1000000, rounds = 100;
    int64_t seed = 1037;
    // one allocation per triple, as the Vec-of-Vecs mirrors do
    Point **triples = malloc(sizeof(Point *) * count);
    for (int64_t i = 0; i < count; i++) {
        Point *p = malloc(sizeof(Point) * 3);
        if (i % 3 == 0) {
            int64_t x = next_random(&seed) % 34, y = next_random(&seed) % 34;
            int64_t dx = next_random(&seed) % 34, dy = next_random(&seed) % 34;
            p[0] = (Point){x, y};
            p[1] = (Point){x + dx, y + dy};
            p[2] = (Point){x + 2 * dx, y + 2 * dy};
        } else {
            for (int k = 0; k < 3; k++) {
                int64_t x = next_random(&seed) % 101;
                int64_t y = next_random(&seed) % 101;
                p[k] = (Point){x, y};
            }
        }
        triples[i] = p;
    }
    int64_t boomerangs = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            bool answer = is_boomerang(triples[i]);
            if (answer) boomerangs++;
            check = (check * 131 + (answer ? 2 : 1)) % 1000000007;
        }
    }
    printf("%lld triples, %lld rounds: %lld boomerangs, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)boomerangs, (long long)check);
    for (int64_t i = 0; i < count; i++) free(triples[i]);
    free(triples);
    return 0;
}
