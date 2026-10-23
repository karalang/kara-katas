// LeetCode #927: Three Equal Parts -- bench: three pointers.
// Mirrors three_equal_parts.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void three_equal_parts(const int64_t *arr, int64_t n, int64_t out[2]) {
    int64_t ones = 0;
    for (int64_t k = 0; k < n; k++) ones += arr[k];
    out[0] = -1;
    out[1] = -1;
    if (ones == 0) {
        out[0] = 0;
        out[1] = n - 1;
        return;
    }
    if (ones % 3 != 0) return;
    int64_t third = ones / 3, starts[3], found = 0, seen = 0;
    for (int64_t k = 0; k < n; k++)
        if (arr[k] == 1) {
            if (seen % third == 0) starts[found++] = k;
            seen++;
        }
    int64_t a = starts[0], b = starts[1], c = starts[2];
    while (c < n && arr[a] == arr[b] && arr[b] == arr[c]) {
        a++;
        b++;
        c++;
    }
    if (c == n) {
        out[0] = a - 1;
        out[1] = b;
    }
}

static int64_t seed = 927;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 30, count = 100, n = 30000;
    // count arrays of 30000 digits, built once: a value of 9000 digits
    // written three times, each copy after up to 1000 leading 0s and the
    // array filled up with 0s in front, and every other array with one
    // digit flipped
    int64_t **arrays = malloc(count * sizeof(int64_t *));
    int64_t *value = malloc(9000 * sizeof(int64_t));
    int64_t *parts = malloc(n * sizeof(int64_t));
    for (int64_t a = 0; a < count; a++) {
        for (int64_t k = 0; k < 9000; k++) value[k] = next_random() % 2;
        int64_t len = 0;
        for (int64_t copy = 0; copy < 3; copy++) {
            int64_t zeros = next_random() % 1001;
            for (int64_t z = 0; z < zeros; z++) parts[len++] = 0;
            for (int64_t k = 0; k < 9000; k++) parts[len++] = value[k];
        }
        arrays[a] = calloc(n, sizeof(int64_t));
        for (int64_t k = 0; k < len; k++) arrays[a][n - len + k] = parts[k];
        if (a % 2 == 1) {
            int64_t at = next_random() % n;
            arrays[a][at] = 1 - arrays[a][at];
        }
    }
    int64_t found = 0, check = 0, got[2];
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every array, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            three_equal_parts(arrays[(r + i) % count], n, got);
            if (got[0] >= 0) found++;
            check = (check * 1000003 + got[0] + 1) % 1000000007;
            check = (check * 1000003 + got[1] + 1) % 1000000007;
        }
    }
    printf("%lld rounds over %lld arrays of 30000: %lld split, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)found, (long long)check);
    for (int64_t a = 0; a < count; a++) free(arrays[a]);
    free(arrays);
    free(value);
    free(parts);
    return 0;
}
