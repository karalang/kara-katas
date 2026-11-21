// LeetCode #2343: Query Kth Smallest Trimmed Number -- the bench, the ★ arm
// in C: for each query the indices sorted by their trimmed text, compared
// in place, and then by index, and the k-th taken.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100
#define W 100

static char nums[10][N][W + 1];
static int64_t queries[10][100][2];
static const char (*cur)[W + 1];
static int64_t cur_from;

static int by_tail(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    int c = memcmp(cur[a] + cur_from, cur[b] + cur_from, W - cur_from);
    if (c != 0) return c;
    return (a > b) - (a < b);
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    for (int64_t c = 0; c < 10; c++) {
        for (int64_t i = 0; i < N; i++) {
            for (int64_t d = 0; d < W; d++) nums[c][i][d] = (char)('0' + scrambled(c * 10000 + i * 100 + d) % 10);
            nums[c][i][W] = 0;
        }
        for (int64_t q = 0; q < 100; q++) {
            queries[c][q][0] = 1 + scrambled(c * 1000 + q + 500000) % 100;
            queries[c][q][1] = 1 + scrambled(c * 1000 + q + 700000) % 100;
        }
    }
    int64_t check = 0;
    int64_t order[N];
    for (int64_t p = 0; p < 50; p++) {
        for (int c = 0; c < 10; c++) {
            for (int q = 0; q < 100; q++) {
                int64_t k = queries[c][q][0], trim = queries[c][q][1];
                for (int64_t i = 0; i < N; i++) order[i] = i;
                cur = (const char (*)[W + 1])nums[c];
                cur_from = W - trim;
                qsort(order, N, sizeof(int64_t), by_tail);
                check = (check * 31 + order[k - 1] + p) % 1000000007;
            }
        }
    }
    printf("50 passes over 10 cases of 100 numbers of 100 digits under 100 queries: checksum %lld\n", (long long)check);
    return 0;
}
