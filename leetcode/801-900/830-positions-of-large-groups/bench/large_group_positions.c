// Benchmark for #830: Positions of Large Groups -- the ★ arm (two pointers).
//
// Mirrors large_group_positions.kara: from the start i of each group, j
// runs on while the letter stays the same, and the group s[i..j] is kept
// when it holds 3 or more. The result is a growable array of pairs, each
// allocated on its own, as the Kāra program's Vec[Vec[i64]] is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t **items;
    int64_t len, cap;
} groups_t;

static void push(groups_t *g, int64_t a, int64_t b) {
    if (g->len == g->cap) {
        g->cap = g->cap ? g->cap * 2 : 4;
        g->items = realloc(g->items, (size_t)g->cap * sizeof(int64_t *));
    }
    int64_t *pair = malloc(2 * sizeof(int64_t));
    pair[0] = a;
    pair[1] = b;
    g->items[g->len++] = pair;
}

static groups_t large_group_positions(const char *s, int64_t n) {
    groups_t groups = {NULL, 0, 0};
    int64_t i = 0;
    while (i < n) {
        int64_t j = i;
        while (j < n && s[j] == s[i]) j++;
        if (j - i >= 3) push(&groups, i, j - 1);
        i = j;
    }
    return groups;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 200000, n = 1000;
    int64_t seed = 830;
    char *strings[64];
    for (int64_t g = 0; g < count; g++) {
        int64_t letters = 1 + g % 3;
        strings[g] = malloc((size_t)n);
        for (int64_t i = 0; i < n; i++) strings[g][i] = (char)('a' + next_random(&seed) % letters);
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        groups_t groups = large_group_positions(strings[round % count], n);
        total += groups.len;
        for (int64_t k = 0; k < groups.len; k++) {
            checksum = (checksum * 131 + groups.items[k][0] * 1009 + groups.items[k][1]) % 1000000007;
            free(groups.items[k]);
        }
        free(groups.items);
    }
    printf("%lld rounds of %lld strings: %lld groups, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) free(strings[g]);
    return 0;
}
