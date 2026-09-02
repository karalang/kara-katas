/* Benchmark mirror — LeetCode 305, Number of Islands II.
 * Same algorithm, same Fisher-Yates over the same LCG, same masked sink as
 * islands2.kara. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 256, cells = n * n, passes = 160;

    int64_t *order = malloc((size_t)cells * sizeof(int64_t));
    for (int64_t i = 0; i < cells; i++) order[i] = i;
    int64_t state = 20305;
    for (int64_t i = cells - 1; i > 0; i--) {
        state = (state * 1103515245 + 12345) % 2147483648;
        int64_t j = state % (i + 1);
        int64_t t = order[i]; order[i] = order[j]; order[j] = t;
    }

    int64_t *parent = malloc((size_t)cells * sizeof(int64_t));
    int64_t *rank = malloc((size_t)cells * sizeof(int64_t));
    int64_t checksum = 0;

    for (int64_t p = 0; p < passes; p++) {
        for (int64_t k = 0; k < cells; k++) { parent[k] = -1; rank[k] = 0; }
        int64_t count = 0;
        for (int64_t q = 0; q < cells; q++) {
            int64_t idx = order[q], r = idx / n, c = idx % n;
            parent[idx] = idx;
            count++;
            for (int64_t d = 0; d < 4; d++) {
                int64_t nb = -1;
                if (d == 0 && r > 0)     nb = idx - n;
                if (d == 1 && r < n - 1) nb = idx + n;
                if (d == 2 && c > 0)     nb = idx - 1;
                if (d == 3 && c < n - 1) nb = idx + 1;
                if (nb >= 0 && parent[nb] >= 0) {
                    int64_t ra = idx, cur, nx;
                    while (parent[ra] != ra) ra = parent[ra];
                    cur = idx;
                    while (parent[cur] != ra) { nx = parent[cur]; parent[cur] = ra; cur = nx; }
                    int64_t rb = nb;
                    while (parent[rb] != rb) rb = parent[rb];
                    cur = nb;
                    while (parent[cur] != rb) { nx = parent[cur]; parent[cur] = rb; cur = nx; }
                    if (ra != rb) {
                        if (rank[ra] < rank[rb]) parent[ra] = rb;
                        else if (rank[ra] > rank[rb]) parent[rb] = ra;
                        else { parent[rb] = ra; rank[ra]++; }
                        count--;
                    }
                }
            }
            checksum = (checksum + count) & 0x3FFFFFFF;
        }
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
