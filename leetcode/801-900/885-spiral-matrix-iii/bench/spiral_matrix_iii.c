// LeetCode #885 bench: C mirror of spiral_matrix_iii.kara (the ★ arm,
// walking the spiral) on the same 6000 grids. The answer is an array of
// pointers to pairs, each pair allocated on its own, as LeetCode's C
// signature returns it.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t **spiral_matrix_iii(int64_t rows, int64_t cols, int64_t r_start, int64_t c_start) {
    static const int64_t dr[4] = {0, 1, 0, -1};
    static const int64_t dc[4] = {1, 0, -1, 0};
    int64_t total = rows * cols;
    int64_t **out = malloc(total * sizeof *out);
    int64_t n = 0;
    out[n] = malloc(2 * sizeof **out);
    out[n][0] = r_start;
    out[n][1] = c_start;
    n++;
    int64_t r = r_start, c = c_start, d = 0, length = 1;
    while (n < total) {
        for (int leg = 0; leg < 2; leg++) {
            for (int64_t s = 0; s < length; s++) {
                r += dr[d];
                c += dc[d];
                if (r >= 0 && r < rows && c >= 0 && c < cols) {
                    out[n] = malloc(2 * sizeof **out);
                    out[n][0] = r;
                    out[n][1] = c;
                    n++;
                }
            }
            d = (d + 1) % 4;
        }
        length++;
    }
    return out;
}

static int64_t seed = 885;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t cells = 0, check = 0;
    for (int g = 0; g < 6000; g++) {
        // 50 x 50 to 100 x 100, the start anywhere
        int64_t rows = 50 + next_random() % 51;
        int64_t cols = 50 + next_random() % 51;
        int64_t r_start = next_random() % rows;
        int64_t c_start = next_random() % cols;
        int64_t **out = spiral_matrix_iii(rows, cols, r_start, c_start);
        int64_t n = rows * cols;
        cells += n;
        check = (check * 131 + out[n - 1][0] * 101 + out[n - 1][1] + out[n / 2][0]) % 1000000007;
        for (int64_t i = 0; i < n; i++) free(out[i]);
        free(out);
    }
    printf("6000 grids of up to 100 x 100: %lld cells, checksum %lld\n", (long long)cells, (long long)check);
    return 0;
}
