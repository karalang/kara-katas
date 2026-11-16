// LeetCode #1172: Dinner Plate Stacks -- the ★ arm's bench in C: the stacks
// in a growable array of growable arrays, and a binary min-heap of the
// indices that may have room, an index whose stack is full or gone dropped
// when it comes to the top. Every array doubles when full and is freed with
// its stream. The same 60 streams of 200000 calls.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *v;
    size_t len, cap;
} Stack;

typedef struct {
    size_t capacity;
    Stack *stacks;
    size_t n, ncap;
    size_t *heap;
    size_t hlen, hcap;
} DinnerPlates;

static void heap_push(DinnerPlates *d, size_t x) {
    if (d->hlen == d->hcap) {
        d->hcap = d->hcap ? 2 * d->hcap : 8;
        d->heap = realloc(d->heap, d->hcap * sizeof *d->heap);
    }
    size_t k = d->hlen++;
    while (k > 0 && d->heap[(k - 1) / 2] > x) {
        d->heap[k] = d->heap[(k - 1) / 2];
        k = (k - 1) / 2;
    }
    d->heap[k] = x;
}

static void heap_pop(DinnerPlates *d) {
    size_t x = d->heap[--d->hlen];
    size_t k = 0;
    for (;;) {
        size_t c = 2 * k + 1;
        if (c >= d->hlen) break;
        if (c + 1 < d->hlen && d->heap[c + 1] < d->heap[c]) c++;
        if (d->heap[c] >= x) break;
        d->heap[k] = d->heap[c];
        k = c;
    }
    if (d->hlen) d->heap[k] = x;
}

static void stack_push(Stack *s, int64_t val) {
    if (s->len == s->cap) {
        s->cap = s->cap ? 2 * s->cap : 4;
        s->v = realloc(s->v, s->cap * sizeof *s->v);
    }
    s->v[s->len++] = val;
}

static void dp_push(DinnerPlates *d, int64_t val) {
    while (d->hlen) {
        size_t i = d->heap[0];
        if (i < d->n && d->stacks[i].len < d->capacity) break;
        heap_pop(d);
    }
    if (!d->hlen) {
        heap_push(d, d->n);
        if (d->n == d->ncap) {
            d->ncap = d->ncap ? 2 * d->ncap : 8;
            d->stacks = realloc(d->stacks, d->ncap * sizeof *d->stacks);
        }
        d->stacks[d->n++] = (Stack){0};
    }
    size_t i = d->heap[0];
    stack_push(&d->stacks[i], val);
    if (d->stacks[i].len == d->capacity) heap_pop(d);
}

static int64_t dp_pop_at_stack(DinnerPlates *d, size_t index) {
    if (index >= d->n || d->stacks[index].len == 0) return -1;
    int64_t val = d->stacks[index].v[--d->stacks[index].len];
    heap_push(d, index);
    while (d->n && d->stacks[d->n - 1].len == 0) free(d->stacks[--d->n].v);
    return val;
}

static int64_t dp_pop(DinnerPlates *d) {
    if (!d->n) return -1;
    return dp_pop_at_stack(d, d->n - 1);
}

static void dp_free(DinnerPlates *d) {
    for (size_t i = 0; i < d->n; i++) free(d->stacks[i].v);
    free(d->stacks);
    free(d->heap);
}

static int64_t seed = 1172;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int streams = 60, calls = 200000;
    size_t capacities[4] = {1, 7, 100, 20000};
    int64_t pops = 0, misses = 0, check = 0;
    for (int s = 0; s < streams; s++) {
        size_t capacity = capacities[s % 4];
        int64_t spread = (int64_t)(20000 / capacity + 1);
        DinnerPlates d = {capacity, 0};
        for (int c = 0; c < calls; c++) {
            int64_t r = next_random() % 10, got;
            if (r < 6) {
                dp_push(&d, 1 + next_random() % 20000);
                continue;
            } else if (r < 8) {
                got = dp_pop(&d);
            } else {
                got = dp_pop_at_stack(&d, (size_t)(next_random() % spread));
            }
            pops++;
            if (got == -1) misses++;
            check = (check * 131 + got + 2) % 1000000007;
        }
        dp_free(&d);
    }
    printf("%d streams of %d calls: %lld pops, %lld empty, checksum %lld\n", streams, calls,
           (long long)pops, (long long)misses, (long long)check);
    return 0;
}
