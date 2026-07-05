/* Bench mirror of spiral_bench.kara — boundary-shrinking spiral over a batch of LCG-filled
 * 24x24 matrices, position-weighted checksum folded into an i64 sink. clang -O3.
 * See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdint.h>

int main(void) {
    int64_t m = 1103515245;       /* glibc LCG multiplier */
    int64_t inc = 12345;          /* glibc LCG increment */
    int64_t modulus = 2147483648; /* 2^31 */
    int64_t windows = 200000;     /* number of simulated input matrices */
    int64_t rows = 24;
    int64_t cols = 24;
    int64_t n = 576;              /* rows * cols */

    int64_t grid[576] = {0};
    int64_t state = 1;            /* LCG seed */
    int64_t sink = 0;
    for (int64_t k = 0; k < windows; k++) {
        for (int64_t idx = 0; idx < n; idx++) {
            state = (state * m + inc) % modulus;
            grid[idx] = (state % 100) - 50;
        }
        int64_t local = 0;
        int64_t pos = 0;
        int64_t top = 0, bottom = rows - 1, left = 0, right = cols - 1;
        while (top <= bottom && left <= right) {
            for (int64_t c = left; c <= right; c++) {
                local += (pos + 1) * grid[top * cols + c];
                pos++;
            }
            top++;
            for (int64_t r = top; r <= bottom; r++) {
                local += (pos + 1) * grid[r * cols + right];
                pos++;
            }
            right--;
            if (top <= bottom) {
                for (int64_t c2 = right; c2 >= left; c2--) {
                    local += (pos + 1) * grid[bottom * cols + c2];
                    pos++;
                }
                bottom--;
            }
            if (left <= right) {
                for (int64_t r2 = bottom; r2 >= top; r2--) {
                    local += (pos + 1) * grid[r2 * cols + left];
                    pos++;
                }
                left++;
            }
        }
        sink += local;
    }
    printf("%lld\n", (long long)sink);
    return 0;
}
