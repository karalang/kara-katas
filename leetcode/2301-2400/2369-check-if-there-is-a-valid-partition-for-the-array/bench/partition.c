// LeetCode #2369: Check if There is a Valid Partition For The Array -- the
// bench, the ★ arm in C: good[i] says whether the first i values split
// into valid blocks, from the last block before i and the values before
// it.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool valid_partition(const int64_t *nums, int64_t n) {
    bool *good = calloc(n + 1, sizeof(bool));
    good[0] = true;
    for (int64_t i = 2; i <= n; i++) {
        int64_t a = nums[i - 1];
        int64_t b = nums[i - 2];
        if (a == b && good[i - 2]) {
            good[i] = true;
        }
        if (i >= 3 && good[i - 3]) {
            int64_t c = nums[i - 3];
            if ((a == b && b == c) || (b == c + 1 && a == b + 1)) {
                good[i] = true;
            }
        }
    }
    bool result = good[n];
    free(good);
    return result;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // array a: about 10^5 values in random blocks of two or three equal
    // values or three rising, the values up to 4^(a + 1); when a is odd, one
    // value near the end then raised by one
    int64_t seed = 2369;
    int64_t *arrays[10];
    int64_t sizes[10];
    int64_t top = 4;
    for (int a = 0; a < 10; a++) {
        arrays[a] = malloc((100000 + 3) * sizeof(int64_t));
        int64_t n = 0;
        while (n < 100000) {
            int64_t kind = next_random(&seed) % 3;
            int64_t hi = next_random(&seed);
            int64_t v = 1 + (hi * 32768 + next_random(&seed)) % top;
            if (kind == 0) {
                arrays[a][n++] = v;
                arrays[a][n++] = v;
            } else if (kind == 1) {
                arrays[a][n++] = v;
                arrays[a][n++] = v;
                arrays[a][n++] = v;
            } else {
                arrays[a][n++] = v;
                arrays[a][n++] = v + 1;
                arrays[a][n++] = v + 2;
            }
        }
        if (a % 2 == 1) {
            int64_t at = n - 1 - next_random(&seed) % 100;
            arrays[a][at] += 1;
        }
        sizes[a] = n;
        top *= 4;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int a = 0; a < 10; a++) {
            int64_t valid = valid_partition(arrays[a], sizes[a]) ? a + 1 : 0;
            check = (check * 31 + valid + p) % 1000000007;
        }
    }
    printf("20 passes over 10 arrays of about 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(arrays[a]);
    }
    return 0;
}
