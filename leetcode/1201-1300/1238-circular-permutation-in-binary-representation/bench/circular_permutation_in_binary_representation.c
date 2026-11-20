// LeetCode #1238: the benchmark, mirroring the Kāra file.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *circular_permutation(int64_t n, int64_t start) {
    int64_t size = (int64_t)1 << n;
    int64_t *p = malloc(sizeof(int64_t) * size);
    for (int64_t i = 0; i < size; i++) p[i] = start ^ i ^ (i >> 1);
    return p;
}

static bool is_cycle(int64_t n, int64_t start, const int64_t *p, int64_t len) {
    int64_t size = (int64_t)1 << n;
    if (len != size || p[0] != start) return false;
    bool *seen = calloc(size, sizeof(bool));
    bool ok = true;
    for (int64_t i = 0; i < size && ok; i++) {
        int64_t v = p[i];
        if (v < 0 || v >= size || seen[v]) ok = false;
        else seen[v] = true;
    }
    free(seen);
    if (!ok) return false;
    for (int64_t i = 0; i < size; i++) {
        int64_t d = p[i] ^ p[(i + 1) % size];
        if (d == 0 || (d & (d - 1)) != 0) return false;
    }
    return true;
}

int main(void) {
    int64_t cycles = 0, check = 0;
    for (int64_t k = 0; k < 64; k++) {
        int64_t start = (k * 1031) % 65536;
        int64_t *p = circular_permutation(16, start);
        if (is_cycle(16, start, p, (int64_t)1 << 16)) cycles++;
        check = (check * 131 + p[32768]) % 1000000007;
        free(p);
    }
    printf("n = 16, 64 starts: %lld cycles, checksum %lld\n", (long long)cycles, (long long)check);
    return 0;
}
