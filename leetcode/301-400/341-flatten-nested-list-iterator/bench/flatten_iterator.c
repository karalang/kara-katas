// Benchmark kernel for LeetCode #341 (Flatten Nested List Iterator).
// Mirrors flatten_iterator.kara: a stack of members, with has_next()
// expanding lists until an integer is on top. 80 rounds, each building a
// pseudo-random nested list of 20,000 top-level members and draining it;
// the sink is a rolling hash of every integer in order.
//
// A member is a tagged struct; a list owns a heap array of members, which
// is freed once its members have been moved onto the stack.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Nested Nested;
struct Nested {
    int is_list;
    int64_t v;
    Nested *items;
    int64_t len, cap;
};

typedef struct {
    Nested *data;
    int64_t len, cap;
} Vec;

static void vec_push(Vec *s, Nested x) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 4;
        s->data = realloc(s->data, (size_t)s->cap * sizeof(Nested));
        if (!s->data) abort();
    }
    s->data[s->len++] = x;
}

typedef struct {
    Vec stack;
} NestedIterator;

// Moves the members of `items` onto the stack in reverse and frees the
// list's array.
static void push_reversed(NestedIterator *it, Nested *items, int64_t len) {
    while (len > 0) vec_push(&it->stack, items[--len]);
    free(items);
}

static int has_next(NestedIterator *it) {
    while (it->stack.len > 0) {
        Nested top = it->stack.data[--it->stack.len];
        if (!top.is_list) {
            it->stack.data[it->stack.len++] = top;
            return 1;
        }
        push_reversed(it, top.items, top.len);
    }
    return 0;
}

static int64_t next(NestedIterator *it) {
    has_next(it);
    if (it->stack.len == 0 || it->stack.data[it->stack.len - 1].is_list) {
        fprintf(stderr, "next() past the end\n");
        abort();
    }
    return it->stack.data[--it->stack.len].v;
}

static int64_t next_rand(int64_t *state) {
    *state = (*state * 1103515245 + 12345) % 2147483648LL;
    return *state >> 8;
}

static Nested gen_member(int64_t *state, int64_t depth, int64_t max_depth) {
    Nested n = {0, 0, NULL, 0, 0};
    if (depth < max_depth && next_rand(state) % 3 == 0) {
        int64_t count = next_rand(state) % 5;
        Vec items = {NULL, 0, 0};
        for (int64_t k = 0; k < count; k++) vec_push(&items, gen_member(state, depth + 1, max_depth));
        n.is_list = 1;
        n.items = items.data;
        n.len = items.len;
        n.cap = items.cap;
        return n;
    }
    n.v = next_rand(state) % 201 - 100;
    return n;
}

static Vec gen_list(int64_t seed, int64_t top, int64_t max_depth) {
    int64_t state = seed;
    Vec items = {NULL, 0, 0};
    for (int64_t k = 0; k < top; k++) vec_push(&items, gen_member(&state, 1, max_depth));
    return items;
}

int main(void) {
    int64_t h = 7;
    for (int64_t r = 0; r < 80; r++) {
        Vec items = gen_list(r * 7 + 1, 20000, 12);
        NestedIterator it = {{NULL, 0, 0}};
        push_reversed(&it, items.data, items.len);
        while (has_next(&it)) h = (h * 31 + next(&it) + 101) % 1000000007;
        free(it.stack.data);
    }
    printf("%lld\n", (long long)h);
    return 0;
}
