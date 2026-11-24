// LeetCode #1337 bench, C mirror of the Kāra bench: the ★ arm on 50
// matrices of 100 by 100 built once, then 2000 passes, each rewriting one
// row of every matrix and choosing k from the checksum so far, answering
// every matrix.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t soldiers;
    int64_t row;
} Pair;

static int by_soldiers_then_row(const void *x, const void *y) {
    const Pair *a = x;
    const Pair *b = y;
    if (a->soldiers != b->soldiers) {
        return a->soldiers < b->soldiers ? -1 : 1;
    }
    return a->row < b->row ? -1 : (a->row > b->row ? 1 : 0);
}

static int64_t soldiers(const int32_t *row, int64_t n) {
    int64_t low = 0;
    int64_t high = n;
    while (low < high) {
        int64_t mid = (low + high) / 2;
        if (row[mid] == 1) {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    return low;
}

// the rows written into out, their count returned
static int64_t k_weakest_rows(int32_t **mat, int64_t m, int64_t n, int32_t k, int32_t *out) {
    Pair *rows = malloc(sizeof(Pair) * m);
    for (int64_t i = 0; i < m; i++) {
        rows[i].soldiers = soldiers(mat[i], n);
        rows[i].row = i;
    }
    qsort(rows, m, sizeof(Pair), by_soldiers_then_row);
    int64_t taken = k < m ? k : m;
    for (int64_t i = 0; i < taken; i++) {
        out[i] = (int32_t)rows[i].row;
    }
    free(rows);
    return taken;
}

static int64_t seed = 1337;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100;
    int32_t **mats[50];
    for (int t = 0; t < 50; t++) {
        mats[t] = malloc(sizeof(int32_t *) * n);
        for (int64_t r = 0; r < n; r++) {
            int64_t s = next_random() % (n + 1);
            mats[t][r] = malloc(sizeof(int32_t) * n);
            for (int64_t c = 0; c < n; c++) {
                mats[t][r][c] = c < s ? 1 : 0;
            }
        }
    }
    int32_t out[100];
    int64_t check = 0;
    for (int64_t pass = 0; pass < 2000; pass++) {
        int32_t k = (int32_t)(1 + check % n);
        for (int t = 0; t < 50; t++) {
            int64_t r = check % n;
            int64_t s = check / 7 % (n + 1);
            for (int64_t c = 0; c < n; c++) {
                mats[t][r][c] = c < s ? 1 : 0;
            }
            int64_t len = k_weakest_rows(mats[t], n, n, k, out);
            check = (check * 31 + out[0] + out[len - 1] + pass) % 1000000007;
        }
    }
    printf("2000 passes over 50 matrices of 100 by 100: checksum %lld\n", (long long)check);
    for (int t = 0; t < 50; t++) {
        for (int64_t r = 0; r < n; r++) {
            free(mats[t][r]);
        }
        free(mats[t]);
    }
    return 0;
}
