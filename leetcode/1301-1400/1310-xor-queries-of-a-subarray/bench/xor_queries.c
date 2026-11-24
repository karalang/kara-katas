// LeetCode #1310 bench, C: the ★ arm (a prefix XOR, each answer the XOR of
// the prefixes at the range's two ends) on the same 10 arrays and 100
// passes. Each answer is a fresh malloc'd array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *xor_queries(const int64_t *arr, int64_t n, const int64_t (*queries)[2], int64_t m) {
    int64_t *prefix = calloc((size_t)n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) prefix[i + 1] = prefix[i] ^ arr[i];
    int64_t *out = malloc(sizeof(int64_t) * (size_t)m);
    for (int64_t k = 0; k < m; k++) out[k] = prefix[queries[k][1] + 1] ^ prefix[queries[k][0]];
    free(prefix);
    return out;
}

static int64_t seed = 1310;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t n = 30000, m = 30000;
    int64_t *arrays[10];
    int64_t (*ranges[10])[2];
    for (int a = 0; a < 10; a++) {
        arrays[a] = malloc(sizeof(int64_t) * (size_t)n);
        for (int64_t k = 0; k < n; k++) {
            int64_t hi = next_random();
            int64_t lo = next_random();
            arrays[a][k] = 1 + (hi * 65536 + lo) % 1000000000;
        }
        ranges[a] = malloc(sizeof(int64_t[2]) * (size_t)m);
        for (int64_t k = 0; k < m; k++) {
            int64_t x = next_random() % n;
            int64_t y = next_random() % n;
            ranges[a][k][0] = x <= y ? x : y;
            ranges[a][k][1] = x <= y ? y : x;
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 100; pass++) {
        for (int a = 0; a < 10; a++) {
            arrays[a][check % n] = 1 + (check / 7) % 1000000000;
            int64_t x = (check / 11) % n, y = (check / 13) % n;
            int64_t at = check % m;
            ranges[a][at][0] = x <= y ? x : y;
            ranges[a][at][1] = x <= y ? y : x;
            int64_t *got = xor_queries(arrays[a], n, (const int64_t (*)[2])ranges[a], m);
            check = (check * 31 + got[(check / 3) % m]) % 1000000007;
            check = (check * 31 + got[(check / 17) % m] + pass) % 1000000007;
            free(got);
        }
    }
    printf("100 passes over 10 arrays of 3 * 10^4: checksum %lld\n", (long long)check);
    return 0;
}
