// LeetCode #1257 bench, in C: the ★ arm (each region's parent in a string
// hash table, the regions holding `region1` in a string hash set, then a
// walk up from `region2` until it meets one of them) on 20 random trees of
// 10000 regions built once, each nested broadly or deeply, with 250 random
// pairs asked of each; every region found folded into a checksum. The
// tables are open-addressed, keyed by the names' bytes, and rebuilt for
// every pair as the other languages' maps are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char **items; int len; } List;

static uint64_t hash_str(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) { h ^= (unsigned char)*s; h *= 1099511628211ULL; }
    return h;
}

typedef struct { char **keys; char **vals; size_t cap; size_t len; } Table;

static void table_init(Table *t, size_t cap) {
    t->cap = cap; t->len = 0;
    t->keys = calloc(cap, sizeof(char *));
    t->vals = calloc(cap, sizeof(char *));
}

static void table_free(Table *t) {
    for (size_t i = 0; i < t->cap; i++) { free(t->keys[i]); free(t->vals[i]); }
    free(t->keys); free(t->vals);
}

static size_t table_slot(const Table *t, const char *k) {
    size_t i = hash_str(k) & (t->cap - 1);
    while (t->keys[i] && strcmp(t->keys[i], k) != 0) i = (i + 1) & (t->cap - 1);
    return i;
}

static void table_grow(Table *t);

static void table_put(Table *t, const char *k, const char *v) {
    if ((t->len + 1) * 2 > t->cap) table_grow(t);
    size_t i = table_slot(t, k);
    if (t->keys[i]) { free(t->vals[i]); }
    else { t->keys[i] = strdup(k); t->len++; }
    t->vals[i] = v ? strdup(v) : NULL;
}

static void table_grow(Table *t) {
    Table n; table_init(&n, t->cap * 2);
    for (size_t i = 0; i < t->cap; i++)
        if (t->keys[i]) {
            size_t j = table_slot(&n, t->keys[i]);
            n.keys[j] = t->keys[i]; n.vals[j] = t->vals[i]; n.len++;
        }
    free(t->keys); free(t->vals);
    *t = n;
}

static const char *table_get(const Table *t, const char *k) {
    size_t i = table_slot(t, k);
    return t->keys[i] ? t->vals[i] : NULL;
}

static int table_has(const Table *t, const char *k) { return t->keys[table_slot(t, k)] != NULL; }

static char *find_smallest_region(const List *regions, int nr, const char *region1, const char *region2) {
    Table parent; table_init(&parent, 16);
    for (int r = 0; r < nr; r++)
        for (int c = 1; c < regions[r].len; c++) table_put(&parent, regions[r].items[c], regions[r].items[0]);
    Table holding; table_init(&holding, 16);
    char *at = strdup(region1);
    table_put(&holding, at, NULL);
    const char *up;
    while ((up = table_get(&parent, at)) != NULL) {
        free(at); at = strdup(up);
        table_put(&holding, at, NULL);
    }
    free(at);
    at = strdup(region2);
    while (!table_has(&holding, at)) {
        const char *p = table_get(&parent, at);
        free(at); at = strdup(p);
    }
    table_free(&parent); table_free(&holding);
    return at;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char *name(int64_t i) {
    char buf[32]; snprintf(buf, sizeof buf, "r%lld", (long long)i);
    return strdup(buf);
}

static List *random_regions(int64_t n, int64_t spread, int64_t *seed, int *count) {
    int64_t *par = malloc(n * sizeof(int64_t));
    int *nkids = calloc(n, sizeof(int));
    for (int64_t i = 1; i < n; i++) {
        int64_t lo = i - spread > 0 ? i - spread : 0;
        par[i] = lo + next_random(seed) % (i - lo);
        nkids[par[i]]++;
    }
    int **kids = malloc(n * sizeof(int *));
    int *fill = calloc(n, sizeof(int));
    for (int64_t p = 0; p < n; p++) kids[p] = malloc((nkids[p] + 1) * sizeof(int));
    for (int64_t i = 1; i < n; i++) kids[par[i]][fill[par[i]]++] = (int)i;
    List *regions = malloc(n * sizeof(List));
    int nr = 0;
    for (int64_t p = 0; p < n; p++) {
        if (nkids[p] == 0) continue;
        List l; l.len = nkids[p] + 1; l.items = malloc(l.len * sizeof(char *));
        l.items[0] = name(p);
        for (int c = 0; c < nkids[p]; c++) l.items[c + 1] = name(kids[p][c]);
        regions[nr++] = l;
    }
    for (int i = nr - 1; i >= 1; i--) {
        int j = (int)(next_random(seed) % (i + 1));
        List tmp = regions[i]; regions[i] = regions[j]; regions[j] = tmp;
    }
    for (int64_t p = 0; p < n; p++) free(kids[p]);
    free(kids); free(fill); free(nkids); free(par);
    *count = nr;
    return regions;
}

int main(void) {
    int64_t seed = 1257;
    const int64_t spreads[4] = {3, 30, 1000000, 10};
    List *trees[20]; int counts[20];
    for (int t = 0; t < 20; t++) trees[t] = random_regions(10000, spreads[t % 4], &seed, &counts[t]);
    int64_t check = 0;
    for (int t = 0; t < 20; t++) {
        for (int q = 0; q < 250; q++) {
            char *x = name(next_random(&seed) % 10000);
            char *y = name(next_random(&seed) % 10000);
            char *found = find_smallest_region(trees[t], counts[t], x, y);
            for (const char *b = found; *b; b++) check = (check * 131 + (unsigned char)*b) % 1000000007;
            free(found); free(x); free(y);
        }
    }
    printf("20 trees of 10000 regions, 250 pairs each: checksum %lld\n", (long long)check);
    return 0;
}
