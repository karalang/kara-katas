// LeetCode #1258 bench, in C: the ★ arm (union-find over the pairs' words
// in a string hash table, the groups sorted, every sentence built by a
// recursive search, the sentences sorted) on 100 random cases built once,
// each 10 pairs of 8 words and a text of 10 words, 4 of them from the
// pairs, asked 80 rounds; the sentences counted and the middle one of each
// answer folded into a checksum. The tables are open-addressed, keyed by
// the words' bytes, and rebuilt for every case as the other languages'
// maps are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint64_t hash_str(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) { h ^= (unsigned char)*s; h *= 1099511628211ULL; }
    return h;
}

// word -> parent word, and word -> its group (filled for roots)
typedef struct { char *key; char *parent; char **group; int ngroup; } Entry;
typedef struct { Entry *e; size_t cap; size_t len; } Table;

static void table_init(Table *t, size_t cap) { t->cap = cap; t->len = 0; t->e = calloc(cap, sizeof(Entry)); }

static void table_free(Table *t) {
    for (size_t i = 0; i < t->cap; i++)
        if (t->e[i].key) {
            free(t->e[i].key); free(t->e[i].parent);
            for (int g = 0; g < t->e[i].ngroup; g++) free(t->e[i].group[g]);
            free(t->e[i].group);
        }
    free(t->e);
}

static size_t slot(const Table *t, const char *k) {
    size_t i = hash_str(k) & (t->cap - 1);
    while (t->e[i].key && strcmp(t->e[i].key, k) != 0) i = (i + 1) & (t->cap - 1);
    return i;
}

static void grow(Table *t) {
    Table n; table_init(&n, t->cap * 2);
    for (size_t i = 0; i < t->cap; i++)
        if (t->e[i].key) { n.e[slot(&n, t->e[i].key)] = t->e[i]; n.len++; }
    free(t->e); *t = n;
}

static Entry *get(Table *t, const char *k) {
    size_t i = slot(t, k);
    return t->e[i].key ? &t->e[i] : NULL;
}

static Entry *put(Table *t, const char *k) {
    if ((t->len + 1) * 2 > t->cap) grow(t);
    size_t i = slot(t, k);
    if (!t->e[i].key) { t->e[i].key = strdup(k); t->len++; }
    return &t->e[i];
}

static char *find(Table *parent, const char *word) {
    Entry *e = get(parent, word);
    if (strcmp(e->parent, word) == 0) return strdup(e->parent);
    char *up = strdup(e->parent);
    char *root = find(parent, up);
    free(up);
    e = get(parent, word);
    free(e->parent); e->parent = strdup(root);
    return root;
}

typedef struct { char **items; size_t len, cap; } Strs;

static void push(Strs *v, char *s) {
    if (v->len == v->cap) { v->cap = v->cap ? v->cap * 2 : 8; v->items = realloc(v->items, v->cap * sizeof(char *)); }
    v->items[v->len++] = s;
}

static int cmp(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }

typedef struct { char **words; int n; } Choice;

static void build(Choice *choices, int nchoices, int at, const char **current, Strs *out) {
    if (at == nchoices) {
        size_t len = 0;
        for (int i = 0; i < nchoices; i++) len += strlen(current[i]) + 1;
        char *s = malloc(len), *p = s;
        for (int i = 0; i < nchoices; i++) {
            if (i) *p++ = ' ';
            size_t l = strlen(current[i]); memcpy(p, current[i], l); p += l;
        }
        *p = 0;
        push(out, s);
        return;
    }
    for (int w = 0; w < choices[at].n; w++) {
        current[at] = choices[at].words[w];
        build(choices, nchoices, at + 1, current, out);
    }
}

typedef struct { char *a, *b; } Pair;

static Strs generate_sentences(Pair *synonyms, int npairs, const char *text) {
    Table parent; table_init(&parent, 16);
    for (int i = 0; i < npairs; i++) {
        const char *w[2] = {synonyms[i].a, synonyms[i].b};
        for (int k = 0; k < 2; k++)
            if (!get(&parent, w[k])) { Entry *e = put(&parent, w[k]); e->parent = strdup(w[k]); }
    }
    for (int i = 0; i < npairs; i++) {
        char *a = find(&parent, synonyms[i].a);
        char *b = find(&parent, synonyms[i].b);
        if (strcmp(a, b) != 0) { Entry *e = get(&parent, a); free(e->parent); e->parent = strdup(b); }
        free(a); free(b);
    }
    Strs words = {0};
    for (size_t i = 0; i < parent.cap; i++) if (parent.e[i].key) push(&words, strdup(parent.e[i].key));
    for (size_t i = 0; i < words.len; i++) {
        char *root = find(&parent, words.items[i]);
        Entry *e = get(&parent, root);
        e->group = realloc(e->group, (e->ngroup + 1) * sizeof(char *));
        e->group[e->ngroup++] = strdup(words.items[i]);
        free(root);
    }
    char *copy = strdup(text);
    Choice choices[16]; int nchoices = 0;
    for (char *tok = strtok(copy, " "); tok; tok = strtok(NULL, " ")) {
        Choice c;
        if (get(&parent, tok)) {
            char *root = find(&parent, tok);
            Entry *e = get(&parent, root);
            c.n = e->ngroup; c.words = malloc(c.n * sizeof(char *));
            for (int g = 0; g < c.n; g++) c.words[g] = strdup(e->group[g]);
            qsort(c.words, c.n, sizeof(char *), cmp);
            free(root);
        } else {
            c.n = 1; c.words = malloc(sizeof(char *)); c.words[0] = strdup(tok);
        }
        choices[nchoices++] = c;
    }
    Strs out = {0};
    const char *current[16];
    build(choices, nchoices, 0, current, &out);
    qsort(out.items, out.len, sizeof(char *), cmp);
    for (int i = 0; i < nchoices; i++) { for (int w = 0; w < choices[i].n; w++) free(choices[i].words[w]); free(choices[i].words); }
    for (size_t i = 0; i < words.len; i++) free(words.items[i]);
    free(words.items); free(copy);
    table_free(&parent);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char *random_word(char first, int64_t *seed) {
    char *w = calloc(4, 1);
    int64_t len = next_random(seed) % 3 + 1;
    for (int64_t i = 0; i < len; i++) w[i] = (char)(first + next_random(seed) % 6);
    return w;
}

static char **random_words(int count, char first, int64_t *seed) {
    char **words = malloc(count * sizeof(char *));
    int n = 0;
    while (n < count) {
        char *w = random_word(first, seed);
        int seen = 0;
        for (int i = 0; i < n; i++) if (strcmp(words[i], w) == 0) seen = 1;
        if (seen) free(w); else words[n++] = w;
    }
    return words;
}

typedef struct { Pair pairs[10]; char *text; } Case;

static Case bench_case(int64_t *seed) {
    Case c;
    char **pool = random_words(8, 'a', seed);
    char **plain = random_words(12, 'p', seed);
    for (int k = 0; k < 10; k++) {
        int64_t i = next_random(seed) % 8;
        int64_t j = (i + 1 + next_random(seed) % 7) % 8;
        c.pairs[k].a = strdup(pool[i]); c.pairs[k].b = strdup(pool[j]);
    }
    const char *words[10];
    for (int k = 0; k < 10; k++) words[k] = plain[next_random(seed) % 12];
    for (int k = 0; k < 4; k++) words[k * 3] = pool[next_random(seed) % 8];
    char buf[64]; buf[0] = 0;
    for (int k = 0; k < 10; k++) { if (k) strcat(buf, " "); strcat(buf, words[k]); }
    c.text = strdup(buf);
    for (int i = 0; i < 8; i++) free(pool[i]);
    for (int i = 0; i < 12; i++) free(plain[i]);
    free(pool); free(plain);
    return c;
}

int main(void) {
    int64_t seed = 1258;
    Case cases[100];
    for (int i = 0; i < 100; i++) cases[i] = bench_case(&seed);
    long total = 0;
    int64_t check = 0;
    for (int r = 0; r < 80; r++)
        for (int i = 0; i < 100; i++) {
            Strs s = generate_sentences(cases[i].pairs, 10, cases[i].text);
            total += (long)s.len;
            for (const char *b = s.items[s.len / 2]; *b; b++) check = (check * 131 + (unsigned char)*b) % 1000000007;
            for (size_t k = 0; k < s.len; k++) free(s.items[k]);
            free(s.items);
        }
    printf("80 rounds of 100 cases: %ld sentences, checksum %lld\n", total, (long long)check);
    return 0;
}
