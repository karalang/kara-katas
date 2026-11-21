// LeetCode #2353: Design a Food Rating System -- the bench, the ★ arm in C:
// lazy heaps. A hash map from each food's name to its rating and its
// cuisine's heap, and a hash map from each cuisine's name to a min-first
// binary heap of (-rating, food) holding every key a food was ever given;
// a query pops the tops that are no longer true. Both maps are open
// addressing with linear probing over FNV-1a of the name, grown at half
// full, and the names are compared with strcmp.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t negated;
    const char *food;
} Entry;

typedef struct {
    Entry *items;
    int64_t len, cap;
} Heap;

static int less(Entry a, Entry b) {
    return a.negated < b.negated || (a.negated == b.negated && strcmp(a.food, b.food) < 0);
}

static void heap_push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 4;
        h->items = realloc(h->items, h->cap * sizeof(Entry));
    }
    Entry *s = h->items;
    int64_t i = h->len++;
    s[i] = e;
    while (i > 0) {
        int64_t up = (i - 1) / 2;
        if (!less(s[i], s[up])) break;
        Entry t = s[i];
        s[i] = s[up];
        s[up] = t;
        i = up;
    }
}

static void heap_pop(Heap *h) {
    Entry *s = h->items;
    s[0] = s[--h->len];
    int64_t i = 0, n = h->len;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && less(s[l], s[m])) m = l;
        if (r < n && less(s[r], s[m])) m = r;
        if (m == i) break;
        Entry t = s[i];
        s[i] = s[m];
        s[m] = t;
        i = m;
    }
}

// A map from a name to a value of `size` bytes.
typedef struct {
    const char **keys;
    char *vals;
    size_t size;
    int64_t cap, len;
} Map;

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) {
        h ^= (unsigned char)*s;
        h *= 1099511628211ULL;
    }
    return h;
}

static void map_init(Map *m, size_t size, int64_t cap) {
    m->size = size;
    m->cap = cap;
    m->len = 0;
    m->keys = calloc(cap, sizeof(char *));
    m->vals = calloc(cap, size);
}

static void *map_slot(Map *m, const char *key, int insert);

static void map_grow(Map *m) {
    Map bigger;
    map_init(&bigger, m->size, 2 * m->cap);
    for (int64_t i = 0; i < m->cap; i++)
        if (m->keys[i]) memcpy(map_slot(&bigger, m->keys[i], 1), m->vals + i * m->size, m->size);
    free(m->keys);
    free(m->vals);
    *m = bigger;
}

// The value slot of key, or NULL when it is absent and insert is 0.
static void *map_slot(Map *m, const char *key, int insert) {
    if (insert && 2 * (m->len + 1) > m->cap) map_grow(m);
    int64_t i = (int64_t)(fnv(key) & (uint64_t)(m->cap - 1));
    while (m->keys[i]) {
        if (strcmp(m->keys[i], key) == 0) return m->vals + i * m->size;
        i = (i + 1) & (m->cap - 1);
    }
    if (!insert) return NULL;
    m->keys[i] = key;
    m->len++;
    return m->vals + i * m->size;
}

typedef struct {
    int64_t rating;
    Heap *heap;
} Food;

typedef struct {
    Map food, cuisine;
} FoodRatings;

static void table_new(FoodRatings *t, char **foods, char **cuisines, const int64_t *ratings, int n) {
    map_init(&t->food, sizeof(Food), 16);
    map_init(&t->cuisine, sizeof(Heap *), 16);
    for (int i = 0; i < n; i++) {
        Heap **h = map_slot(&t->cuisine, cuisines[i], 1);
        if (!*h) *h = calloc(1, sizeof(Heap));
        Heap *heap = *h;
        Food *f = map_slot(&t->food, foods[i], 1);
        f->rating = ratings[i];
        f->heap = heap;
        heap_push(heap, (Entry){-ratings[i], foods[i]});
    }
}

static void table_free(FoodRatings *t) {
    for (int64_t i = 0; i < t->cuisine.cap; i++) {
        if (t->cuisine.keys[i]) {
            Heap *h = *(Heap **)(t->cuisine.vals + i * sizeof(Heap *));
            free(h->items);
            free(h);
        }
    }
    free(t->food.keys);
    free(t->food.vals);
    free(t->cuisine.keys);
    free(t->cuisine.vals);
}

static void change_rating(FoodRatings *t, const char *food, int64_t rating) {
    Food *f = map_slot(&t->food, food, 0);
    f->rating = rating;
    heap_push(f->heap, (Entry){-rating, food});
}

static const char *highest_rated(FoodRatings *t, const char *cuisine) {
    Heap *h = *(Heap **)map_slot(&t->cuisine, cuisine, 0);
    for (;;) {
        Entry top = h->items[0];
        Food *f = map_slot(&t->food, top.food, 0);
        if (f->rating == -top.negated) return top.food;
        heap_pop(h);
    }
}

static int64_t seed = 2353;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define N 10000
#define CALLS 100000

int main(void) {
    static char *foods[N], *cuisines[N];
    static int64_t ratings[N];
    for (int64_t i = 0; i < N; i++) {
        int64_t v = i * 7919 % 456976;
        foods[i] = malloc(5);
        foods[i][0] = (char)(97 + v / 17576);
        foods[i][1] = (char)(97 + v / 676 % 26);
        foods[i][2] = (char)(97 + v / 26 % 26);
        foods[i][3] = (char)(97 + v % 26);
        foods[i][4] = 0;
    }
    for (int i = 0; i < N; i++) {
        cuisines[i] = malloc(8);
        snprintf(cuisines[i], 8, "c%lld", (long long)(next_random() % 100));
    }
    for (int i = 0; i < N; i++) ratings[i] = 1 + next_random() % 100000000;
    static int64_t kind[CALLS], rating[CALLS];
    static char *name[CALLS];
    for (int i = 0; i < CALLS; i++) {
        int64_t f = next_random() % N;
        if (i % 3 == 2) {
            kind[i] = 1;
            name[i] = strdup(cuisines[f]);
            rating[i] = 0;
        } else {
            kind[i] = 0;
            name[i] = strdup(foods[f]);
            rating[i] = 1 + next_random() % 100000000;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++) {
        FoodRatings t;
        table_new(&t, foods, cuisines, ratings, N);
        for (int i = 0; i < CALLS; i++) {
            if (kind[i] == 0) {
                change_rating(&t, name[i], rating[i]);
            } else {
                for (const char *b = highest_rated(&t, name[i]); *b; b++) check = (check * 31 + (unsigned char)*b) % 1000000007;
                check = (check * 31 + p) % 1000000007;
            }
        }
        table_free(&t);
    }
    printf("100 passes over 10^4 foods and 10^5 calls: checksum %lld\n", (long long)check);
    return 0;
}
