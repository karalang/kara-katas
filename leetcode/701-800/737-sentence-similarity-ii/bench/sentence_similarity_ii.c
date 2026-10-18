// LeetCode #737: Sentence Similarity II -- union-find.
// Benchmark mirror of the Kara star arm: number every word in a pair,
// join the two words of each pair in a union-find with union by size
// and path compression, and compare the roots of the two words at each
// place. The table that numbers the words holds pointers to them rather
// than copies, as C would, and Go's and Python's maps share the words
// too; the Kara and Rust programs copy each word into theirs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *w;
    int64_t id;
} Slot;

typedef struct {
    Slot *slots;
    uint64_t cap, len;
} Table;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static int64_t *table_get(Table *t, const char *w) {
    uint64_t i = hash(w) & (t->cap - 1);
    while (t->slots[i].w) {
        if (strcmp(t->slots[i].w, w) == 0) return &t->slots[i].id;
        i = (i + 1) & (t->cap - 1);
    }
    return NULL;
}

static void table_put(Table *t, const char *w, int64_t id) {
    if ((t->len + 1) * 2 > t->cap) {
        Table bigger = {calloc(t->cap * 2, sizeof(Slot)), t->cap * 2, 0};
        for (uint64_t i = 0; i < t->cap; i++)
            if (t->slots[i].w) table_put(&bigger, t->slots[i].w, t->slots[i].id);
        free(t->slots);
        *t = bigger;
    }
    uint64_t i = hash(w) & (t->cap - 1);
    while (t->slots[i].w) i = (i + 1) & (t->cap - 1);
    t->slots[i] = (Slot){w, id};
    t->len++;
}

typedef struct {
    int64_t *parent, *size;
    int64_t len, cap;
} Forest;

static int64_t find(Forest *f, int64_t x) {
    int64_t root = x;
    while (f->parent[root] != root) root = f->parent[root];
    while (f->parent[x] != root) {
        int64_t next = f->parent[x];
        f->parent[x] = root;
        x = next;
    }
    return root;
}

static int64_t number(Table *t, Forest *f, const char *w) {
    int64_t *got = table_get(t, w);
    if (got) return *got;
    if (f->len == f->cap) {
        f->cap = f->cap ? f->cap * 2 : 16;
        f->parent = realloc(f->parent, f->cap * sizeof(int64_t));
        f->size = realloc(f->size, f->cap * sizeof(int64_t));
    }
    int64_t i = f->len++;
    f->parent[i] = i;
    f->size[i] = 1;
    table_put(t, w, i);
    return i;
}

static int are_sentences_similar_two(char **s1, char **s2, int64_t n1, int64_t n2, char **pa, char **pb, int64_t np) {
    if (n1 != n2) return 0;
    Table t = {calloc(16, sizeof(Slot)), 16, 0};
    Forest f = {0, 0, 0, 0};
    for (int64_t k = 0; k < np; k++) {
        int64_t a = number(&t, &f, pa[k]);
        int64_t b = number(&t, &f, pb[k]);
        int64_t ra = find(&f, a), rb = find(&f, b);
        if (ra != rb) {
            if (f.size[ra] < f.size[rb]) {
                f.parent[ra] = rb;
                f.size[rb] += f.size[ra];
            } else {
                f.parent[rb] = ra;
                f.size[ra] += f.size[rb];
            }
        }
    }
    int ok = 1;
    for (int64_t i = 0; i < n1 && ok; i++) {
        if (strcmp(s1[i], s2[i]) == 0) continue;
        int64_t *a = table_get(&t, s1[i]);
        int64_t *b = table_get(&t, s2[i]);
        if (!a || !b || find(&f, *a) != find(&f, *b)) ok = 0;
    }
    free(t.slots);
    free(f.parent);
    free(f.size);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *word(int64_t k) {
    char *s = malloc(16);
    snprintf(s, 16, "w%lld", (long long)k);
    return s;
}

int main(void) {
    int64_t seed = 737;
    char *pa[2000], *pb[2000];
    int64_t *near[3000];
    int64_t nnear[3000] = {0}, cnear[3000] = {0};
    for (int k = 0; k < 3000; k++) near[k] = NULL;
    for (int k = 0; k < 2000; k++) {
        int64_t a = next_random(&seed) % 3000;
        int64_t b = next_random(&seed) % 3000;
        pa[k] = word(a);
        pb[k] = word(b);
        int64_t ends[2][2] = {{a, b}, {b, a}};
        for (int e = 0; e < 2; e++) {
            int64_t u = ends[e][0], v = ends[e][1];
            if (nnear[u] == cnear[u]) {
                cnear[u] = cnear[u] ? cnear[u] * 2 : 4;
                near[u] = realloc(near[u], cnear[u] * sizeof(int64_t));
            }
            near[u][nnear[u]++] = v;
        }
    }
    char *s1[1000], *s2[1000];
    for (int k = 0; k < 1000; k++) {
        int64_t start = next_random(&seed) % 3000;
        int64_t at = start;
        int64_t steps = next_random(&seed) % 6;
        for (int64_t t = 0; t < steps; t++)
            if (nnear[at] > 0) at = near[at][next_random(&seed) % nnear[at]];
        s1[k] = word(start);
        s2[k] = word(at);
    }
    int similar = 0;
    for (int r = 0; r < 1000; r++) {
        int64_t j = next_random(&seed) % 1000;
        int64_t x = next_random(&seed) % 3000;
        char *saved = s2[j];
        s2[j] = word(x);
        if (are_sentences_similar_two(s1, s2, 1000, 1000, pa, pb, 2000)) similar++;
        free(s2[j]);
        s2[j] = saved;
        if (are_sentences_similar_two(s1, s2, 1000, 1000, pa, pb, 2000)) similar++;
    }
    printf("1000 rounds of 2 checks of 1000 words with 2000 pairs: %d similar\n", similar);
    for (int k = 0; k < 2000; k++) free(pa[k]), free(pb[k]);
    for (int k = 0; k < 1000; k++) free(s1[k]), free(s2[k]);
    for (int k = 0; k < 3000; k++) free(near[k]);
    return 0;
}
