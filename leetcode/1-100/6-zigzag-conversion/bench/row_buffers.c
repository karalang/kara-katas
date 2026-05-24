/*
 * LeetCode 6 — row-buffer Zigzag Conversion, C mirror.
 * Algorithmic peer of bench/row_buffers.{kara,rs,py}. Same N, R, K,
 * num_rows, same input pattern, same sink formula.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static void convert_off(const char *chars, size_t off, size_t len, size_t num_rows,
                        char *out, size_t *out_len) {
    if (num_rows <= 1 || num_rows >= len) {
        for (size_t i = 0; i < len; i++) {
            out[i] = chars[off + i];
        }
        *out_len = len;
        return;
    }

    char **rows = (char **)malloc(num_rows * sizeof(char *));
    size_t *row_lens = (size_t *)calloc(num_rows, sizeof(size_t));
    size_t *row_caps = (size_t *)calloc(num_rows, sizeof(size_t));
    for (size_t r = 0; r < num_rows; r++) {
        row_caps[r] = 64;
        rows[r] = (char *)malloc(row_caps[r]);
    }

    size_t cur = 0;
    int going_down = 0;
    for (size_t i = 0; i < len; i++) {
        if (row_lens[cur] == row_caps[cur]) {
            row_caps[cur] *= 2;
            rows[cur] = (char *)realloc(rows[cur], row_caps[cur]);
        }
        rows[cur][row_lens[cur]++] = chars[off + i];
        if (cur == 0 || cur == num_rows - 1) {
            going_down = !going_down;
        }
        if (going_down) {
            cur++;
        } else {
            cur--;
        }
    }

    size_t pos = 0;
    for (size_t r = 0; r < num_rows; r++) {
        memcpy(out + pos, rows[r], row_lens[r]);
        pos += row_lens[r];
        free(rows[r]);
    }
    *out_len = pos;
    free(rows);
    free(row_lens);
    free(row_caps);
}

int main(void) {
    const size_t n = 10000;
    const size_t r_period = 1000;
    const size_t k_iters = 10000;
    const size_t num_rows = 4;

    static const char pattern[] = "PAYPALISHIRING";
    const size_t pattern_len = sizeof(pattern) - 1;
    const size_t need = n + r_period;

    char *chars = (char *)malloc(need + pattern_len);
    size_t filled = 0;
    while (filled < need) {
        memcpy(chars + filled, pattern, pattern_len);
        filled += pattern_len;
    }

    char *result = (char *)malloc(n);
    size_t result_len;

    int64_t sum = 0;
    for (size_t k = 0; k < k_iters; k++) {
        size_t off = k % r_period;
        convert_off(chars, off, n, num_rows, result, &result_len);
        sum += (int64_t)(unsigned char)result[0]
             + (int64_t)(unsigned char)result[result_len - 1];
    }
    printf("%lld\n", (long long)sum);

    free(result);
    free(chars);
    return 0;
}
