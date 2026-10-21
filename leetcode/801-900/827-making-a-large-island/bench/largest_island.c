// Benchmark for #827: Making A Large Island -- the ★ arm (label, then try each 0).
//
// Mirrors largest_island.kara: a breadth-first search on a queue gives
// every island a label and records its size, and each 0 adds 1 to the
// sizes of the distinct labels around it. The grid and the labels are
// arrays of rows, as the Kāra program's Vec[Vec[i64]] is, and the labels,
// sizes and queue are fresh each call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t largest_island(int64_t **grid, int64_t n) {
    int64_t **label = malloc((size_t)n * sizeof(int64_t *));
    for (int64_t r = 0; r < n; r++) label[r] = calloc((size_t)n, sizeof(int64_t));
    int64_t size_cap = 16, size_len = 0;
    int64_t *size = malloc((size_t)size_cap * sizeof(int64_t));
    int64_t *qr = malloc((size_t)(n * n) * sizeof(int64_t));
    int64_t *qc = malloc((size_t)(n * n) * sizeof(int64_t));
    static const int64_t dr[4] = {-1, 1, 0, 0};
    static const int64_t dc[4] = {0, 0, -1, 1};
    for (int64_t r = 0; r < n; r++) {
        for (int64_t c = 0; c < n; c++) {
            if (grid[r][c] == 1 && label[r][c] == 0) {
                int64_t id = size_len + 1;
                label[r][c] = id;
                int64_t head = 0, tail = 0;
                qr[tail] = r;
                qc[tail++] = c;
                int64_t count = 0;
                while (head < tail) {
                    int64_t cr = qr[head], cc = qc[head++];
                    count++;
                    for (int k = 0; k < 4; k++) {
                        int64_t nr = cr + dr[k], nc = cc + dc[k];
                        if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == 1 && label[nr][nc] == 0) {
                            label[nr][nc] = id;
                            qr[tail] = nr;
                            qc[tail++] = nc;
                        }
                    }
                }
                if (size_len == size_cap) {
                    size_cap *= 2;
                    size = realloc(size, (size_t)size_cap * sizeof(int64_t));
                }
                size[size_len++] = count;
            }
        }
    }
    int64_t best = 0;
    for (int64_t i = 0; i < size_len; i++)
        if (size[i] > best) best = size[i];
    for (int64_t r = 0; r < n; r++) {
        for (int64_t c = 0; c < n; c++) {
            if (grid[r][c] == 0) {
                int64_t seen[4];
                int64_t seen_len = 0;
                int64_t made = 1;
                for (int k = 0; k < 4; k++) {
                    int64_t nr = r + dr[k], nc = c + dc[k];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n) {
                        int64_t id = label[nr][nc];
                        int found = 0;
                        for (int64_t s = 0; s < seen_len; s++)
                            if (seen[s] == id) found = 1;
                        if (id > 0 && !found) {
                            seen[seen_len++] = id;
                            made += size[id - 1];
                        }
                    }
                }
                if (made > best) best = made;
            }
        }
    }
    for (int64_t r = 0; r < n; r++) free(label[r]);
    free(label);
    free(size);
    free(qr);
    free(qc);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 16;
    int64_t rounds = 200;
    int64_t n = 500;
    int64_t seed = 827;
    int64_t **grids[16];
    for (int64_t g = 0; g < count; g++) {
        grids[g] = malloc((size_t)n * sizeof(int64_t *));
        for (int64_t r = 0; r < n; r++) {
            grids[g][r] = malloc((size_t)n * sizeof(int64_t));
            for (int64_t c = 0; c < n; c++) grids[g][r][c] = next_random(&seed) % 100 < 55 ? 1 : 0;
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t r = largest_island(grids[round % count], n);
        total += r;
        checksum = (checksum * 131 + r) % 1000000007;
    }
    printf("%lld rounds of %lld grids: total %lld, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)total, (long long)checksum);
    return 0;
}
