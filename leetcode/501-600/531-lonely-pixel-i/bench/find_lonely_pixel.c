// Benchmark for #531: C mirror of the ★ arm (count each row and column);
// see find_lonely_pixel.kara. A picture is one flat array of bytes, and
// each answer allocates its two count arrays, as the ★ arm's `vec!`s.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_lonely_pixel(const char *picture, int64_t m, int64_t n) {
    int64_t *rows = calloc(m, sizeof(int64_t));
    int64_t *cols = calloc(n, sizeof(int64_t));
    for (int64_t r = 0; r < m; r++) {
        for (int64_t c = 0; c < n; c++) {
            if (picture[r * n + c] == 'B') {
                rows[r]++;
                cols[c]++;
            }
        }
    }
    int64_t lonely = 0;
    for (int64_t r = 0; r < m; r++) {
        for (int64_t c = 0; c < n; c++) {
            if (picture[r * n + c] == 'B' && rows[r] == 1 && cols[c] == 1) lonely++;
        }
    }
    free(rows);
    free(cols);
    return lonely;
}

int main(void) {
    // 20 pictures of 500 by 500 made once, black with a chance of 1 to 20
    // in 1,000; then every picture is answered 200 times.
    int64_t seed = 531;
    char *pictures[20];
    for (int p = 0; p < 20; p++) {
        int64_t per_mille = 1 + p;
        pictures[p] = malloc(500 * 500);
        for (int i = 0; i < 500 * 500; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            pictures[p][i] = seed / 65536 % 1000 < per_mille ? 'B' : 'W';
        }
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < 200; round++) {
        for (int p = 0; p < 20; p++) {
            int64_t answer = find_lonely_pixel(pictures[p], 500, 500);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    printf("20 pictures of 500 by 500, 200 times each: total %lld, checksum %lld\n", (long long)total,
           (long long)checksum);
    for (int p = 0; p < 20; p++) free(pictures[p]);
    return 0;
}
