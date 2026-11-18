// LeetCode #2312: Selling Pieces of Wood -- the bench, the ★ arm in C.
// Bottom up over every size: each piece its own price or the most of
// any one cut across it.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { LISTS = 10, PRICES = 2000, SIDE = 200 };

typedef struct { int64_t h, w, price; } Price;

static int64_t best[SIDE + 1][SIDE + 1];

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t selling_wood(int64_t m, int64_t n, const Price *prices, int64_t count) {
    for (int64_t h = 0; h <= m; h++)
        for (int64_t w = 0; w <= n; w++)
            best[h][w] = 0;
    for (int64_t k = 0; k < count; k++)
        best[prices[k].h][prices[k].w] = prices[k].price;
    for (int64_t h = 1; h <= m; h++) {
        for (int64_t w = 1; w <= n; w++) {
            for (int64_t i = 1; i < h; i++)
                best[h][w] = max64(best[h][w], best[i][w] + best[h - i][w]);
            for (int64_t j = 1; j < w; j++)
                best[h][w] = max64(best[h][w], best[h][j] + best[h][w - j]);
        }
    }
    return best[m][n];
}

static int64_t seed = 2312;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static Price lists[LISTS][PRICES];
    static int64_t counts[LISTS];
    static bool used[SIDE * SIDE];
    for (int a = 0; a < LISTS; a++) {
        memset(used, 0, sizeof used);
        counts[a] = 0;
        for (int k = 0; k < PRICES; k++) {
            int64_t h = next_random() % SIDE + 1;
            int64_t w = next_random() % SIDE + 1;
            int64_t price = next_random() % 1000000 + 1;
            if (!used[(h - 1) * SIDE + w - 1]) {
                used[(h - 1) * SIDE + w - 1] = true;
                lists[a][counts[a]++] = (Price){h, w, price};
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 2; p++) {
        for (int a = 0; a < LISTS; a++) {
            Price *prices = malloc(sizeof(Price) * (size_t)counts[a]);
            for (int64_t k = 0; k < counts[a]; k++)
                prices[k] = (Price){lists[a][k].h, lists[a][k].w, lists[a][k].price + p};
            check = (check * 31 + selling_wood(SIDE, SIDE, prices, counts[a])) % 1000000007;
            free(prices);
        }
    }
    printf("2 passes over 10 lists of 2000 prices on 200 by 200: checksum %lld\n", (long long)check);
    return 0;
}
