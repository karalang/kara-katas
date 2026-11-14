// LeetCode #1152 bench -- mirrors most_visited_pattern.kara: the same
// 64 problems, the same rounds, the ★ arm's maps and sets, here as
// open-addressing hash tables keyed by string contents (FNV-1a). The
// strings are shared, not copied, as Go and Python share them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { const char *s[3]; } Tri;

static uint64_t fnv(uint64_t h, const char *s) {
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return (h ^ 0xff) * 1099511628211ULL;
}

static uint64_t tri_hash(const Tri *t) {
    uint64_t h = 14695981039346656037ULL;
    for (int i = 0; i < 3; i++) h = fnv(h, t->s[i]);
    return h;
}

static int tri_cmp(const Tri *a, const Tri *b) {
    for (int i = 0; i < 3; i++) {
        int c = strcmp(a->s[i], b->s[i]);
        if (c) return c;
    }
    return 0;
}

// A table of triples, each with a count; `used` marks a filled slot.
typedef struct {
    Tri *keys;
    int64_t *vals;
    char *used;
    size_t cap, len;
} Table;

static void table_init(Table *t, size_t cap) {
    t->cap = cap;
    t->len = 0;
    t->keys = malloc(cap * sizeof(Tri));
    t->vals = malloc(cap * sizeof(int64_t));
    t->used = calloc(cap, 1);
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->vals);
    free(t->used);
}

static int64_t *table_slot(Table *t, const Tri *k, int *fresh);

static void table_grow(Table *t) {
    Table old = *t;
    table_init(t, old.cap * 2);
    for (size_t i = 0; i < old.cap; i++) {
        if (old.used[i]) {
            int fresh;
            *table_slot(t, &old.keys[i], &fresh) = old.vals[i];
        }
    }
    table_free(&old);
}

// The count for `k`, a new slot set to 0 if `k` is absent.
static int64_t *table_slot(Table *t, const Tri *k, int *fresh) {
    if ((t->len + 1) * 4 > t->cap * 3) table_grow(t);
    size_t i = tri_hash(k) & (t->cap - 1);
    while (t->used[i]) {
        if (tri_cmp(&t->keys[i], k) == 0) {
            *fresh = 0;
            return &t->vals[i];
        }
        i = (i + 1) & (t->cap - 1);
    }
    t->used[i] = 1;
    t->keys[i] = *k;
    t->vals[i] = 0;
    t->len++;
    *fresh = 1;
    return &t->vals[i];
}

typedef struct { const char *name; const char *sites[50]; int n; } User;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

// The ★ arm: `n` visits, each user's sites in time order, the set of
// patterns per user, the scores, the best and the smallest among ties.
static Tri most_visited_pattern(const char **username, const int64_t *timestamp, const char **website, int n) {
    int order[64];
    for (int i = 0; i < n; i++) order[i] = i;
    // insertion sort by time (n <= 50)
    for (int i = 1; i < n; i++) {
        int x = order[i], j = i;
        while (j > 0 && timestamp[order[j - 1]] > timestamp[x]) {
            order[j] = order[j - 1];
            j--;
        }
        order[j] = x;
    }
    User users[64];
    int nu = 0;
    for (int k = 0; k < n; k++) {
        int i = order[k], u = 0;
        while (u < nu && strcmp(users[u].name, username[i]) != 0) u++;
        if (u == nu) {
            users[nu].name = username[i];
            users[nu].n = 0;
            nu++;
        }
        users[u].sites[users[u].n++] = website[i];
    }
    Table score;
    table_init(&score, 64);
    for (int u = 0; u < nu; u++) {
        int m = users[u].n;
        const char **s = users[u].sites;
        Table seen;
        table_init(&seen, 64);
        for (int a = 0; a < m; a++)
            for (int b = a + 1; b < m; b++)
                for (int c = b + 1; c < m; c++) {
                    Tri t = {{s[a], s[b], s[c]}};
                    int fresh;
                    table_slot(&seen, &t, &fresh);
                }
        for (size_t i = 0; i < seen.cap; i++) {
            if (seen.used[i]) {
                int fresh;
                *table_slot(&score, &seen.keys[i], &fresh) += 1;
            }
        }
        table_free(&seen);
    }
    Tri best = {{0, 0, 0}};
    int64_t top = -1;
    for (size_t i = 0; i < score.cap; i++) {
        if (!score.used[i]) continue;
        int64_t s = score.vals[i];
        if (s > top || (s == top && tri_cmp(&score.keys[i], &best) < 0)) {
            top = s;
            best = score.keys[i];
        }
    }
    table_free(&score);
    return best;
}

int main(void) {
    int rounds = 5000;
    char site_names[8][8], user_names[5][8];
    for (int s = 0; s < 8; s++) snprintf(site_names[s], 8, "site%d", s);
    for (int u = 0; u < 5; u++) snprintf(user_names[u], 8, "user%d", u);
    int64_t seed = 1152;
    static const char *username[64][50], *website[64][50];
    static int64_t timestamp[64][50];
    for (int p = 0; p < 64; p++) {
        for (int i = 0; i < 50; i++) username[p][i] = user_names[next_random(&seed) % 5];
        for (int i = 0; i < 50; i++) website[p][i] = site_names[next_random(&seed) % 8];
        for (int i = 0; i < 50; i++) timestamp[p][i] = i + 1;
        for (int j = 49; j >= 1; j--) {
            int k = next_random(&seed) % (j + 1);
            int64_t x = timestamp[p][j];
            timestamp[p][j] = timestamp[p][k];
            timestamp[p][k] = x;
        }
    }
    int64_t distinct = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        int p = r % 64;
        for (int q = 0; q < 4; q++) {
            int at = next_random(&seed) % 50;
            website[p][at] = site_names[next_random(&seed) % 8];
        }
        Tri a = most_visited_pattern(username[p], timestamp[p], website[p], 50);
        if (strcmp(a.s[0], a.s[1]) && strcmp(a.s[1], a.s[2]) && strcmp(a.s[0], a.s[2])) distinct++;
        for (int i = 0; i < 3; i++)
            for (const char *c = a.s[i]; *c; c++) check = (check * 31 + (unsigned char)*c) % 1000000007;
    }
    printf("%d rounds over 64 problems of 50 visits: %lld patterns of three sites, checksum %lld\n", rounds,
           (long long)distinct, (long long)check);
    return 0;
}
