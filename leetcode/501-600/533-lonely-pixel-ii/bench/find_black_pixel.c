// Benchmark for #533: C mirror of the ★ arm (count each kind of row); see
// find_black_pixel.kara. Each row is copied into a fresh key buffer, as
// the ★ arm builds a `String` per row. C has no map, so each call builds
// a fresh open-addressing table of those keys (FNV-1a over the bytes,
// linear probing) that owns them until the call ends.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t m, n;
    char *cells;
} Picture;

static uint64_t fnv(const char *s, int64_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (int64_t i = 0; i < n; i++) h = (h ^ (unsigned char)s[i]) * 1099511628211ULL;
    return h;
}

static int64_t find_black_pixel(const Picture *p, int64_t target) {
    int64_t m = p->m, n = p->n;
    int64_t *cols = calloc(n, sizeof(int64_t));
    uint64_t size = 1;
    while (size < 2 * (uint64_t)m) size *= 2;
    char **slot_key = calloc(size, sizeof(char *));
    int64_t *slot_count = calloc(size, sizeof(int64_t));
    for (int64_t r = 0; r < m; r++) {
        const char *row = p->cells + r * n;
        char *key = malloc(n);
        int64_t blacks = 0;
        for (int64_t c = 0; c < n; c++) {
            key[c] = row[c];
            if (row[c] == 'B') {
                cols[c]++;
                blacks++;
            }
        }
        if (blacks != target) {
            free(key);
            continue;
        }
        uint64_t i = fnv(key, n) & (size - 1);
        while (slot_key[i] && memcmp(slot_key[i], key, n) != 0) i = (i + 1) & (size - 1);
        if (slot_key[i]) {
            free(key);
        } else {
            slot_key[i] = key;
        }
        slot_count[i]++;
    }
    int64_t lonely = 0;
    for (uint64_t i = 0; i < size; i++) {
        if (!slot_key[i]) continue;
        if (slot_count[i] == target) {
            for (int64_t c = 0; c < n; c++) {
                if (slot_key[i][c] == 'B' && cols[c] == target) lonely += target;
            }
        }
        free(slot_key[i]);
    }
    free(cols);
    free(slot_key);
    free(slot_count);
    return lonely;
}

static int64_t seed = 533;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static Picture random_picture(int64_t n, int64_t target, int64_t planted, int64_t extra, int64_t percent) {
    int64_t cap = planted * (target + 1) + extra;
    char *cells = malloc(cap * n);
    int64_t m = 0;
    int64_t *cols = malloc(n * sizeof(int64_t));
    char *row = malloc(n);
    for (int64_t k = 0; k < planted; k++) {
        for (int64_t c = 0; c < n; c++) {
            cols[c] = c;
            row[c] = 'W';
        }
        for (int64_t i = 0; i < target; i++) {
            int64_t j = i + next_random() % (n - i);
            int64_t x = cols[i];
            cols[i] = cols[j];
            cols[j] = x;
            row[cols[i]] = 'B';
        }
        int64_t copies = next_random() % 4 == 0 ? target + 1 : target;
        for (int64_t c = 0; c < copies; c++) memcpy(cells + (m++) * n, row, n);
    }
    for (int64_t k = 0; k < extra; k++) {
        for (int64_t c = 0; c < n; c++) cells[m * n + c] = next_random() % 100 < percent ? 'B' : 'W';
        m++;
    }
    for (int64_t i = m - 1; i > 0; i--) {
        int64_t j = next_random() % (i + 1);
        memcpy(row, cells + i * n, n);
        memcpy(cells + i * n, cells + j * n, n);
        memcpy(cells + j * n, row, n);
    }
    free(cols);
    free(row);
    return (Picture){m, n, cells};
}

int main(void) {
    // 20 pictures 200 wide made once, the p-th with 20 rows planted for a
    // target of 1 + p % 8 and 80 more black with a chance of 1%; then
    // each picture is answered for every target from 1 to 8, in 100
    // rounds.
    Picture pictures[20];
    for (int p = 0; p < 20; p++) pictures[p] = random_picture(200, 1 + p % 8, 20, 80, 1);
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < 100; round++) {
        for (int p = 0; p < 20; p++) {
            for (int64_t target = 1; target <= 8; target++) {
                int64_t answer = find_black_pixel(&pictures[p], target);
                total += answer;
                checksum = (checksum * 31 + answer) % 1000000007;
            }
        }
    }
    printf("20 pictures 200 wide, targets 1 to 8, 100 rounds: total %lld, checksum %lld\n", (long long)total,
           (long long)checksum);
    for (int p = 0; p < 20; p++) free(pictures[p].cells);
    return 0;
}
