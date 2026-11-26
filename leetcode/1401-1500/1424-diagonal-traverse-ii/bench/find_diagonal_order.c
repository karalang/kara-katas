#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* A growable array of int32, as a Vec[i32]. */
typedef struct {
    int32_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int32_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, sizeof(int32_t) * v->cap);
    }
    v->data[v->len++] = x;
}

/* The order into `order`, its buckets one Vec each, as the Kara arm's. */
static void find_diagonal_order(const Vec *nums, int64_t rows, Vec *order) {
    Vec *diagonals = NULL;
    int64_t count = 0, cap = 0;
    for (int64_t i = rows - 1; i >= 0; i--) {
        for (int64_t j = 0; j < nums[i].len; j++) {
            while (count <= i + j) {
                if (count == cap) {
                    cap = cap ? cap * 2 : 4;
                    diagonals = realloc(diagonals, sizeof(Vec) * cap);
                }
                memset(&diagonals[count], 0, sizeof(Vec));
                count++;
            }
            push(&diagonals[i + j], nums[i].data[j]);
        }
    }
    order->len = 0;
    for (int64_t d = 0; d < count; d++) {
        for (int64_t k = 0; k < diagonals[d].len; k++) push(order, diagonals[d].data[k]);
        free(diagonals[d].data);
    }
    free(diagonals);
}

int main(void) {
    int64_t seed = 1424;
    Vec *pool = calloc(100000, sizeof(Vec));
    for (int r = 0; r < 100000; r++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t n = 1 + seed / 65536 % 9;
        for (int64_t k = 0; k < n; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            push(&pool[r], (int32_t)(1 + seed / 65536 % 100000));
        }
    }
    int64_t check = 0;
    for (int w = 0; w < 300; w++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t start = seed / 65536 % 80001;
        Vec order = {0};
        find_diagonal_order(pool + start, 20000, &order);
        for (int64_t k = 0; k < order.len; k++) check = (check * 131 + order.data[k]) % 1000000007;
        free(order.data);
    }
    printf("300 windows of 2 * 10^4 rows: checksum %lld\n", (long long)check);
    for (int r = 0; r < 100000; r++) free(pool[r].data);
    free(pool);
    return 0;
}
