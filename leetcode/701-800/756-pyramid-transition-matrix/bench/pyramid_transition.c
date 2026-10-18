// LeetCode 756 — Pyramid Transition Matrix: benchmark, the ★ arm in C.
// The memo of dead rows is an open-addressing hash set made per call.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *slots; // 0 marks an empty slot; row codes are at least 1
    size_t cap, len;
} Set;

static size_t slot_of(int64_t key, size_t cap) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (size_t)(h >> 32) & (cap - 1);
}

static bool set_contains(const Set *s, int64_t key) {
    for (size_t i = slot_of(key, s->cap);; i = (i + 1) & (s->cap - 1)) {
        if (s->slots[i] == key) return true;
        if (s->slots[i] == 0) return false;
    }
}

static void set_insert(Set *s, int64_t key);

static void set_grow(Set *s) {
    Set bigger = {calloc(s->cap * 2, sizeof(int64_t)), s->cap * 2, 0};
    for (size_t i = 0; i < s->cap; i++)
        if (s->slots[i] != 0) set_insert(&bigger, s->slots[i]);
    free(s->slots);
    *s = bigger;
}

static void set_insert(Set *s, int64_t key) {
    if (2 * (s->len + 1) > s->cap) set_grow(s);
    size_t i = slot_of(key, s->cap);
    while (s->slots[i] != 0) {
        if (s->slots[i] == key) return;
        i = (i + 1) & (s->cap - 1);
    }
    s->slots[i] = key;
    s->len++;
}

typedef struct {
    int64_t *items;
    size_t len, cap;
} Row;

static void row_push(Row *r, int64_t x) {
    if (r->len == r->cap) {
        r->cap = r->cap ? r->cap * 2 : 4;
        r->items = realloc(r->items, r->cap * sizeof(int64_t));
    }
    r->items[r->len++] = x;
}

static int64_t row_code(const Row *row) {
    int64_t code = 1;
    for (size_t i = 0; i < row->len; i++) code = code * 6 + row->items[i];
    return code;
}

static bool build(const Row *row, const int64_t *table, Set *dead);

static bool fill(const Row *row, size_t i, Row *next, const int64_t *table, Set *dead) {
    if (i + 1 == row->len) return build(next, table, dead);
    int64_t options = table[row->items[i] * 6 + row->items[i + 1]];
    int64_t block = 0;
    while (options > 0) {
        if ((options & 1) == 1) {
            row_push(next, block);
            if (fill(row, i + 1, next, table, dead)) return true;
            next->len--;
        }
        options >>= 1;
        block++;
    }
    return false;
}

static bool build(const Row *row, const int64_t *table, Set *dead) {
    if (row->len == 1) return true;
    int64_t code = row_code(row);
    if (set_contains(dead, code)) return false;
    Row next = {0};
    bool ok = fill(row, 0, &next, table, dead);
    free(next.items);
    if (ok) return true;
    set_insert(dead, code);
    return false;
}

static bool pyramid_transition(const char *bottom, char (*allowed)[4], int count) {
    int64_t table[36] = {0};
    for (int t = 0; t < count; t++) {
        int pair = (allowed[t][0] - 'A') * 6 + (allowed[t][1] - 'A');
        table[pair] |= (int64_t)1 << (allowed[t][2] - 'A');
    }
    Row row = {0};
    for (const char *c = bottom; *c; c++) row_push(&row, *c - 'A');
    Set dead = {calloc(16, sizeof(int64_t)), 16, 0};
    bool ok = build(&row, table, &dead);
    free(dead.slots);
    free(row.items);
    return ok;
}

static int64_t seed = 756;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rounds = 200000, yes = 0, check = 0;
    char allowed[120][4];
    for (int64_t round = 0; round < rounds; round++) {
        char bottom[7];
        for (int i = 0; i < 6; i++) bottom[i] = (char)('A' + next_random() % 6);
        bottom[6] = 0;
        int count = (int)(40 + next_random() % 80);
        for (int t = 0; t < count; t++) {
            for (int j = 0; j < 3; j++) allowed[t][j] = (char)('A' + next_random() % 6);
            allowed[t][3] = 0;
        }
        if (pyramid_transition(bottom, allowed, count)) {
            yes++;
            check = (check * 31 + round) % 1000000007;
        }
    }
    printf("%lld pyramids of width 6: %lld can be built, checksum %lld\n", (long long)rounds,
           (long long)yes, (long long)check);
    return 0;
}
