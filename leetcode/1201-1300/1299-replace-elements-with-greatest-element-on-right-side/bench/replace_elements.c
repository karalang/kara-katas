// LeetCode #1299 bench: the ★ arm (one walk from the right end, each place
// given the greatest seen so far) over 50 arrays of 10^4 numbers up to 10^5,
// built once; then 1000 passes, each setting one number of every array from the
// checksum so far, answering it, and folding two of its answers, chosen by the
// checksum, into the checksum. Each answer is a fresh malloc, as the other
// languages' are fresh arrays.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *replace_elements(const int64_t *arr, int64_t n) {
    int64_t *out = malloc(sizeof(int64_t) * n);
    int64_t greatest = -1;
    for (int64_t i = n - 1; i >= 0; i--) {
        out[i] = greatest;
        if (arr[i] > greatest) greatest = arr[i];
    }
    return out;
}

static int64_t seed = 1299;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *arrays[50];
    for (int t = 0; t < 50; t++) {
        arrays[t] = malloc(sizeof(int64_t) * 10000);
        for (int j = 0; j < 10000; j++) {
            int64_t hi = next_random();
            arrays[t][j] = 1 + (hi * 32768 + next_random()) % 100000;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 1000; p++) {
        for (int t = 0; t < 50; t++) {
            arrays[t][check % 10000] = 1 + check * 7919 % 100000;
            int64_t *out = replace_elements(arrays[t], 10000);
            check = (check * 31 + out[check % 10000] + out[(check / 7) % 10000] + p) % 1000000007;
            free(out);
        }
    }
    printf("1000 passes over 50 arrays of 10^4: checksum %lld\n", (long long)check);
    for (int t = 0; t < 50; t++) free(arrays[t]);
    return 0;
}
