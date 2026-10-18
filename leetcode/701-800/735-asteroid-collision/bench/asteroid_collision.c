// LeetCode #735: Asteroid Collision -- a stack of survivors.
// Benchmark mirror of the Kara star arm: walk the row keeping the
// survivors so far on a stack; a left-mover destroys the smaller
// right-movers on top, then is destroyed by a larger one, dies with an
// equal one, or survives onto the stack.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static Vec asteroid_collision(const int64_t *asteroids, int64_t n) {
    Vec stack = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) {
        int64_t a = asteroids[i];
        int alive = 1;
        while (alive && a < 0 && stack.len > 0 && stack.data[stack.len - 1] > 0) {
            int64_t top = stack.data[stack.len - 1];
            if (top < -a) {
                stack.len--;
            } else {
                if (top == -a) stack.len--;
                alive = 0;
            }
        }
        if (alive) push(&stack, a);
    }
    return stack;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 735;
    int64_t *rows[20];
    for (int k = 0; k < 20; k++) {
        rows[k] = malloc(10000 * sizeof(int64_t));
        for (int i = 0; i < 10000; i++) {
            int64_t size = 1 + next_random(&seed) % 1000;
            rows[k][i] = next_random(&seed) % 2 == 0 ? size : -size;
        }
    }
    int64_t left = 0, sum = 0;
    for (int r = 0; r < 500; r++) {
        for (int k = 0; k < 20; k++) {
            int64_t j = next_random(&seed) % 10000;
            rows[k][j] = -rows[k][j];
            Vec survivors = asteroid_collision(rows[k], 10000);
            left += survivors.len;
            for (int64_t i = 0; i < survivors.len; i++) sum = (sum * 31 + survivors.data[i] + 1000) % 1000000007;
            free(survivors.data);
        }
    }
    printf("500 rounds of 20 rows of 10000 asteroids: %lld left, checksum %lld\n", (long long)left, (long long)sum);
    for (int k = 0; k < 20; k++) free(rows[k]);
    return 0;
}
