// Benchmark for #364 -- mirror of weight_sum.kara. A list is an array of
// tagged items; an item is an integer or a pointer to a list.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct List List;
typedef struct {
    int is_int;
    int64_t v;
    List *inner;
} Item;
struct List {
    int64_t len, cap;
    Item *items;
};

static void push(List *l, Item it) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, (size_t)l->cap * sizeof(Item));
    }
    l->items[l->len++] = it;
}

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t max_depth(const List *l, int64_t depth) {
    int64_t deepest = 0;
    for (int64_t i = 0; i < l->len; i++) {
        const Item *it = &l->items[i];
        if (it->is_int) deepest = max64(deepest, depth);
        else deepest = max64(deepest, max_depth(it->inner, depth + 1));
    }
    return deepest;
}

static int64_t weighted(const List *l, int64_t depth, int64_t top) {
    int64_t total = 0;
    for (int64_t i = 0; i < l->len; i++) {
        const Item *it = &l->items[i];
        if (it->is_int) total += it->v * (top - depth + 1);
        else total += weighted(it->inner, depth + 1, top);
    }
    return total;
}

static int64_t depth_sum_inverse(const List *l) { return weighted(l, 1, max_depth(l, 1)); }

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static List *build(int64_t *seed, int64_t depth) {
    int64_t n = next(seed) % 13;
    List *out = calloc(1, sizeof(List));
    for (int64_t i = 0; i < n; i++) {
        if (depth < 14 && next(seed) % 3 == 0) {
            Item it = {0, 0, build(seed, depth + 1)};
            push(out, it);
        } else {
            Item it = {1, next(seed) % 201 - 100, NULL};
            push(out, it);
        }
    }
    return out;
}

static void release(List *l) {
    for (int64_t i = 0; i < l->len; i++)
        if (!l->items[i].is_int) release(l->items[i].inner);
    free(l->items);
    free(l);
}

int main(void) {
    int64_t seed = 364, checksum = 0;
    for (int t = 0; t < 10; t++) {
        List *l = build(&seed, 1);
        for (int r = 0; r < 20; r++)
            checksum = (checksum * 31 + depth_sum_inverse(l) + 1000000000000000LL) % 1000000007;
        release(l);
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
