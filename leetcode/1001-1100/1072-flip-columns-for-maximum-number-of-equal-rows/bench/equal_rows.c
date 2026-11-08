// LeetCode #1072: Flip Columns For Maximum Number of Equal Rows -- the
// benchmark's C mirror of equal_rows.kara: the same count of row patterns,
// each row's key built as a string of '0's and '1's and counted in an
// open-addressing hash table keyed by FNV-1a, over 200 matrices built once,
// each answered 30 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t m, n;
    int64_t *cells;  // m rows of n cells
} matrix;

typedef struct {
    char *key;  // NULL when the slot is empty
    int64_t count;
} slot;

static uint64_t fnv1a(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < n; i++) {
        h ^= (unsigned char)s[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static int64_t max_equal_rows(const matrix *mx) {
    int64_t size = 1;
    while (size < 2 * mx->m) size *= 2;
    slot *table = calloc(size, sizeof(slot));
    int64_t best = 0;
    for (int64_t i = 0; i < mx->m; i++) {
        const int64_t *row = mx->cells + i * mx->n;
        char *key = malloc(mx->n);
        for (int64_t j = 0; j < mx->n; j++) key[j] = row[j] != row[0] ? '1' : '0';
        uint64_t at = fnv1a(key, mx->n) & (size - 1);
        while (table[at].key && memcmp(table[at].key, key, mx->n) != 0) at = (at + 1) & (size - 1);
        if (table[at].key) {
            free(key);
        } else {
            table[at].key = key;
        }
        int64_t seen = ++table[at].count;
        if (seen > best) best = seen;
    }
    for (int64_t i = 0; i < size; i++) free(table[i].key);
    free(table);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static matrix random_matrix(int64_t rows, int64_t cols, int64_t *seed) {
    matrix mx;
    mx.m = next_random(seed) % rows + 1;
    mx.n = next_random(seed) % cols + 1;
    int64_t count = next_random(seed) % 3 + 1;
    int64_t *patterns = malloc(count * mx.n * sizeof(int64_t));
    for (int64_t p = 0; p < count; p++)
        for (int64_t j = 0; j < mx.n; j++) patterns[p * mx.n + j] = next_random(seed) % 2;
    mx.cells = malloc(mx.m * mx.n * sizeof(int64_t));
    for (int64_t i = 0; i < mx.m; i++) {
        int64_t *row = mx.cells + i * mx.n;
        int64_t roll = next_random(seed) % 8;
        if (roll < 2) {
            for (int64_t j = 0; j < mx.n; j++) row[j] = next_random(seed) % 2;
        } else {
            const int64_t *p = patterns + (next_random(seed) % count) * mx.n;
            for (int64_t j = 0; j < mx.n; j++) row[j] = roll < 5 ? 1 - p[j] : p[j];
        }
    }
    free(patterns);
    return mx;
}

int main(void) {
    int64_t seed = 1072;
    matrix matrices[200];
    for (int i = 0; i < 200; i++) matrices[i] = random_matrix(300, 300, &seed);
    int64_t total = 0, check = 0;
    for (int r = 0; r < 30; r++) {
        for (int i = 0; i < 200; i++) {
            int64_t x = max_equal_rows(&matrices[i]);
            total += x;
            check = (check * 31 + x) % 1000000007;
        }
    }
    printf("6000 calls: answers sum %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int i = 0; i < 200; i++) free(matrices[i].cells);
    return 0;
}
