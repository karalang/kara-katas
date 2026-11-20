// LeetCode #1727: Largest Submatrix With Rearrangements -- the bench
// (submatrix.kara): each row's column heights sorted, the k-th from the
// shortest giving a submatrix n - k wide.
//
// The heights sorted by qsort, where Kāra and Rust use a stable merge
// sort and Go `sort.Slice`; any sort gives the same sorted heights.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20
#define ROUNDS 50
#define SIDE 316

static int ascending(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static int32_t largest_submatrix(const int32_t (*matrix)[SIDE], int m, int n) {
    int32_t heights[SIDE] = {0};
    int32_t sorted[SIDE];
    int32_t best = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            heights[j] = matrix[i][j] == 1 ? heights[j] + 1 : 0;
        }
        memcpy(sorted, heights, sizeof(int32_t) * n);
        qsort(sorted, n, sizeof(int32_t), ascending);
        for (int k = 0; k < n; k++) {
            int32_t area = sorted[k] * (n - k);
            if (area > best) {
                best = area;
            }
        }
    }
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    static int32_t problems[COUNT][SIDE][SIDE];
    int64_t seed = 1727;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < SIDE; i++) {
            for (int j = 0; j < SIDE; j++) {
                problems[c][i][j] = next_random(&seed) % 8 == 0 ? 0 : 1;
            }
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = largest_submatrix((const int32_t (*)[SIDE])problems[c], SIDE, SIDE);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d matrices of %d by %d, %d rounds: areas sum to %lld, checksum %lld\n", COUNT, SIDE, SIDE, ROUNDS,
           (long long)sum, (long long)check);
    return 0;
}
