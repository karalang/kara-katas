// LeetCode #1334 bench, C mirror of the Kāra bench: the ★ arm on 10 maps
// of 100 cities built once, then 30 passes, each setting one road's weight
// of every map and the threshold from the checksum so far, answering every
// map.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t find_the_city(int32_t n, int32_t (*edges)[3], size_t m, int32_t distance_threshold) {
    const int64_t far = 1000000000;
    int64_t *dist = malloc(sizeof(int64_t) * n * n);
    for (int32_t i = 0; i < n * n; i++) {
        dist[i] = far;
    }
    for (int32_t i = 0; i < n; i++) {
        dist[i * n + i] = 0;
    }
    for (size_t e = 0; e < m; e++) {
        dist[edges[e][0] * n + edges[e][1]] = edges[e][2];
        dist[edges[e][1] * n + edges[e][0]] = edges[e][2];
    }
    for (int32_t k = 0; k < n; k++) {
        for (int32_t i = 0; i < n; i++) {
            for (int32_t j = 0; j < n; j++) {
                if (dist[i * n + k] + dist[k * n + j] < dist[i * n + j]) {
                    dist[i * n + j] = dist[i * n + k] + dist[k * n + j];
                }
            }
        }
    }
    int32_t best = 0;
    int32_t fewest = n + 1;
    for (int32_t i = 0; i < n; i++) {
        int32_t near = 0;
        for (int32_t j = 0; j < n; j++) {
            if (j != i && dist[i * n + j] <= distance_threshold) {
                near++;
            }
        }
        if (near <= fewest) {
            fewest = near;
            best = i;
        }
    }
    free(dist);
    return best;
}

static int64_t seed = 1334;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int32_t n = 100;
    int32_t (*maps[10])[3];
    size_t sizes[10];
    for (int t = 0; t < 10; t++) {
        maps[t] = malloc(sizeof(int32_t[3]) * n * n / 2);
        size_t m = 0;
        for (int32_t a = 0; a < n; a++) {
            for (int32_t b = a + 1; b < n; b++) {
                if (next_random() % 2 == 0) {
                    maps[t][m][0] = a;
                    maps[t][m][1] = b;
                    maps[t][m][2] = (int32_t)(1 + next_random() % 10000);
                    m++;
                }
            }
        }
        sizes[t] = m;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 30; pass++) {
        int32_t threshold = (int32_t)(200 + check % 800);
        for (int t = 0; t < 10; t++) {
            int64_t at = check % (int64_t)sizes[t];
            maps[t][at][2] = (int32_t)(1 + check / 3 % 10000);
            int32_t city = find_the_city(n, maps[t], sizes[t], threshold);
            check = (check * 31 + city + pass) % 1000000007;
        }
    }
    printf("30 passes over 10 maps of 100 cities: checksum %lld\n", (long long)check);
    for (int t = 0; t < 10; t++) {
        free(maps[t]);
    }
    return 0;
}
