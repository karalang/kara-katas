// LeetCode #716: Max Stack -- a stack of running maxima beside it.
// Benchmark mirror of the Kara star arm: each value with the largest
// value at or below it; pop_max pops into a buffer until the max is on
// top, drops it, and pushes the buffer back.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Vec;

static void vpush(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? 2 * v->cap : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

typedef struct {
    Vec values, maxes;
} MaxStack;

static void push(MaxStack *s, int64_t x) {
    int64_t m = x;
    if (s->maxes.len > 0 && s->maxes.data[s->maxes.len - 1] > x) m = s->maxes.data[s->maxes.len - 1];
    vpush(&s->values, x);
    vpush(&s->maxes, m);
}

static int64_t pop(MaxStack *s) {
    s->maxes.len--;
    return s->values.data[--s->values.len];
}

static int64_t top(const MaxStack *s) { return s->values.data[s->values.len - 1]; }

static int64_t peek_max(const MaxStack *s) { return s->maxes.data[s->maxes.len - 1]; }

static int64_t pop_max(MaxStack *s) {
    int64_t m = peek_max(s);
    Vec buffer = {0};
    while (top(s) != m) vpush(&buffer, pop(s));
    pop(s);
    while (buffer.len > 0) push(s, buffer.data[--buffer.len]);
    free(buffer.data);
    return m;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

enum { LISTS = 10, CALLS = 100000 };

int main(void) {
    int64_t seed = 716;
    static int64_t kinds[LISTS][CALLS], xs[LISTS][CALLS];
    for (int l = 0; l < LISTS; l++) {
        int64_t size = 0;
        for (int c = 0; c < CALLS; c++) {
            if (size == 0 || next_random(&seed) % 2 == 0) {
                int64_t hi = next_random(&seed);
                int64_t lo = next_random(&seed);
                kinds[l][c] = 0;
                xs[l][c] = (hi * 32768 + lo) % 1000001;
                size++;
            } else {
                int64_t kind = 1 + next_random(&seed) % 4;
                kinds[l][c] = kind;
                xs[l][c] = 0;
                if (kind == 1 || kind == 4) size--;
            }
        }
    }
    int64_t sum = 0;
    for (int round = 0; round < 10; round++) {
        for (int l = 0; l < LISTS; l++) {
            MaxStack s = {0};
            for (int c = 0; c < CALLS; c++) {
                int64_t kind = kinds[l][c];
                if (kind == 0) push(&s, xs[l][c]);
                else if (kind == 1) sum += pop(&s);
                else if (kind == 2) sum += top(&s);
                else if (kind == 3) sum += peek_max(&s);
                else sum += pop_max(&s);
            }
            free(s.values.data);
            free(s.maxes.data);
        }
    }
    printf("10 rounds of 10 lists of 100000 calls: sum %lld\n", (long long)sum);
    return 0;
}
