// Benchmark for #661: each cell's 3x3 window, as the Kara ★ arm. Each
// pass allocates its output rows, as the Kara program does, and frees
// the input's.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t **image_smoother(int64_t **img, int64_t m, int64_t n) {
    int64_t **out = malloc(m * sizeof *out);
    for (int64_t i = 0; i < m; i++) {
        out[i] = malloc(n * sizeof **out);
        for (int64_t j = 0; j < n; j++) {
            int64_t sum = 0, count = 0;
            int64_t r0 = i - 1 > 0 ? i - 1 : 0, r1 = i + 2 < m ? i + 2 : m;
            int64_t c0 = j - 1 > 0 ? j - 1 : 0, c1 = j + 2 < n ? j + 2 : n;
            for (int64_t r = r0; r < r1; r++) {
                for (int64_t c = c0; c < c1; c++) {
                    sum += img[r][c];
                    count++;
                }
            }
            out[i][j] = sum / count;
        }
    }
    return out;
}

static int64_t seed = 661;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t size = 1000, passes = 20;
    int64_t **img = malloc(size * sizeof *img);
    for (int64_t i = 0; i < size; i++) {
        img[i] = malloc(size * sizeof **img);
        for (int64_t j = 0; j < size; j++) img[i][j] = next_random() % 256;
    }
    for (int64_t p = 0; p < passes; p++) {
        int64_t **next = image_smoother(img, size, size);
        for (int64_t i = 0; i < size; i++) free(img[i]);
        free(img);
        img = next;
    }
    int64_t checksum = 0;
    for (int64_t i = 0; i < size; i++)
        for (int64_t j = 0; j < size; j++) checksum = (checksum * 31 + img[i][j]) % 1000000007;
    printf("%lldx%lld, %lld passes: checksum %lld\n", (long long)size, (long long)size, (long long)passes,
           (long long)checksum);
    for (int64_t i = 0; i < size; i++) free(img[i]);
    free(img);
    return 0;
}
