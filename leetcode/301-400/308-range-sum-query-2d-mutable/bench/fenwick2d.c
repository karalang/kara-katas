/* Benchmark mirror — LeetCode 308, Range Sum Query 2D (Mutable).
 * Same 2D Fenwick tree, same LCG-generated operation script, same masked sink
 * as fenwick2d.kara. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void) {
    const int64_t n = 256, stride = n + 1, ops = 100000, passes = 54;
    int64_t *tree = calloc((size_t)((n + 1) * stride), sizeof(int64_t));
    int64_t *data = calloc((size_t)(n * n), sizeof(int64_t));
    int64_t *kind = malloc((size_t)ops * sizeof(int64_t));
    int64_t *o1 = malloc((size_t)ops * sizeof(int64_t));
    int64_t *o2 = malloc((size_t)ops * sizeof(int64_t));
    int64_t *o3 = malloc((size_t)ops * sizeof(int64_t));
    int64_t *o4 = malloc((size_t)ops * sizeof(int64_t));

    int64_t state = 20308;
    for (int64_t k = 0; k < ops; k++) {
        state = (state * 1103515245 + 12345) % 2147483648; int64_t t = state % 2;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t a = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t b = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t c = state % n;
        state = (state * 1103515245 + 12345) % 2147483648; int64_t d = state % n;
        kind[k] = t;
        if (t == 0) { o1[k] = a; o2[k] = b; o3[k] = c % 2001 - 1000; o4[k] = 0; }
        else {
            if (a <= c) { o1[k] = a; o3[k] = c; } else { o1[k] = c; o3[k] = a; }
            if (b <= d) { o2[k] = b; o4[k] = d; } else { o2[k] = d; o4[k] = b; }
        }
    }

    int64_t checksum = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int64_t k = 0; k < ops; k++) {
            if (kind[k] == 0) {
                int64_t r = o1[k], c = o2[k];
                int64_t delta = o3[k] - data[r * n + c];
                data[r * n + c] = o3[k];
                for (int64_t x = r + 1; x <= n; x += x & -x)
                    for (int64_t y = c + 1; y <= n; y += y & -y)
                        tree[x * stride + y] += delta;
            } else {
                int64_t r1 = o1[k], c1 = o2[k], r2 = o3[k] + 1, c2 = o4[k] + 1;
                int64_t total = 0;
                for (int64_t qi = 0; qi < 4; qi++) {
                    int64_t px = r2, py = c2, sign = 1;
                    if (qi == 1) { px = r1; sign = -1; }
                    if (qi == 2) { py = c1; sign = -1; }
                    if (qi == 3) { px = r1; py = c1; }
                    int64_t sub = 0;
                    for (int64_t x = px; x > 0; x -= x & -x)
                        for (int64_t y = py; y > 0; y -= y & -y)
                            sub += tree[x * stride + y];
                    total += sign * sub;
                }
                checksum = (checksum + total) & 0x3FFFFFFF;
            }
        }
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
