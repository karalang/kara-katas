/* Benchmark mirror for LeetCode #244 - Shortest Word Distance II.
 *
 * Same algorithm, same LCG, same sink as the Kara/Rust/Go/Python mirrors:
 * build the 20,000-word list and its position index ONCE (index-pool
 * construction - word -> slot in a hash map, plus a side array of position
 * arrays), then punch 200,000 two-pointer merge queries.
 *
 * The map is a REAL dynamic open-addressing hash table that grows on load
 * factor, not a fixed-capacity table sized to the known vocabulary. A
 * pre-sized table would hand C a free win the other four lanes do not get,
 * since each of them pays for a general-purpose map.
 *
 * Keys are the 9-byte words; every one shares the 5-byte prefix "delta", so
 * FNV-1a walks the whole key and no comparison exits early. Equality is a
 * fixed-length memcmp for the same reason the Kara side avoids length
 * shortcuts.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define VOCAB_N 256
#define N 20000
#define ITERS 200000
#define WORD_LEN 9

/* ---- dynamic open-addressing map: 9-byte key -> int slot ---- */

typedef struct {
    const char *key; /* NULL = empty */
    int slot;
} Entry;

typedef struct {
    Entry *tab;
    size_t cap;  /* power of two */
    size_t len;
} Map;

static uint64_t fnv1a(const char *p) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < WORD_LEN; i++) {
        h ^= (unsigned char)p[i];
        h *= 1099511628211ULL;
    }
    return h;
}

static void map_init(Map *m) {
    m->cap = 16;
    m->len = 0;
    m->tab = calloc(m->cap, sizeof(Entry));
}

static void map_put(Map *m, const char *key, int slot);

static void map_grow(Map *m) {
    Entry *old = m->tab;
    size_t oldcap = m->cap;
    m->cap *= 2;
    m->len = 0;
    m->tab = calloc(m->cap, sizeof(Entry));
    for (size_t i = 0; i < oldcap; i++)
        if (old[i].key) map_put(m, old[i].key, old[i].slot);
    free(old);
}

static void map_put(Map *m, const char *key, int slot) {
    if ((m->len + 1) * 4 >= m->cap * 3) map_grow(m);
    size_t mask = m->cap - 1;
    size_t i = (size_t)fnv1a(key) & mask;
    while (m->tab[i].key) {
        if (memcmp(m->tab[i].key, key, WORD_LEN) == 0) {
            m->tab[i].slot = slot;
            return;
        }
        i = (i + 1) & mask;
    }
    m->tab[i].key = key;
    m->tab[i].slot = slot;
    m->len++;
}

/* Returns the slot, or -1 when absent. */
static int map_get(const Map *m, const char *key) {
    size_t mask = m->cap - 1;
    size_t i = (size_t)fnv1a(key) & mask;
    while (m->tab[i].key) {
        if (memcmp(m->tab[i].key, key, WORD_LEN) == 0) return m->tab[i].slot;
        i = (i + 1) & mask;
    }
    return -1;
}

/* ---- the index ---- */

typedef struct {
    long *pos;
    size_t len;
    size_t cap;
} List;

typedef struct {
    Map slot;
    List *lists;
    size_t nlists;
    size_t listcap;
    long size;
} WordDistance;

static void list_push(List *l, long v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->pos = realloc(l->pos, l->cap * sizeof(long));
    }
    l->pos[l->len++] = v;
}

static void wd_build(WordDistance *wd, char **words, long n) {
    map_init(&wd->slot);
    wd->nlists = 0;
    wd->listcap = 16;
    wd->lists = calloc(wd->listcap, sizeof(List));
    wd->size = n;
    for (long i = 0; i < n; i++) {
        int s = map_get(&wd->slot, words[i]);
        if (s >= 0) {
            list_push(&wd->lists[s], i);
        } else {
            if (wd->nlists == wd->listcap) {
                wd->listcap *= 2;
                wd->lists = realloc(wd->lists, wd->listcap * sizeof(List));
                memset(wd->lists + wd->nlists, 0,
                       (wd->listcap - wd->nlists) * sizeof(List));
            }
            List *fresh = &wd->lists[wd->nlists];
            fresh->pos = NULL;
            fresh->len = 0;
            fresh->cap = 0;
            list_push(fresh, i);
            map_put(&wd->slot, words[i], (int)wd->nlists);
            wd->nlists++;
        }
    }
}

static long wd_shortest(const WordDistance *wd, const char *w1, const char *w2) {
    int s1 = map_get(&wd->slot, w1);
    if (s1 < 0) return wd->size;
    int s2 = map_get(&wd->slot, w2);
    if (s2 < 0) return wd->size;
    const List *p1 = &wd->lists[s1];
    const List *p2 = &wd->lists[s2];
    long best = wd->size;
    size_t a = 0, b = 0;
    while (a < p1->len && b < p2->len) {
        long d = p1->pos[a] - p2->pos[b];
        if (d < 0) d = -d;
        if (d < best) best = d;
        if (p1->pos[a] < p2->pos[b]) a++;
        else b++;
    }
    return best;
}

static long lcg(long state) {
    return (state * 1103515245L + 12345L) & 2147483647L;
}

int main(void) {
    static const char alpha[4] = {'a', 'b', 'c', 'd'};

    char (*vocab)[WORD_LEN + 1] = malloc(VOCAB_N * (WORD_LEN + 1));
    for (int v = 0; v < VOCAB_N; v++) {
        memcpy(vocab[v], "delta", 5);
        vocab[v][5] = alpha[(v / 64) % 4];
        vocab[v][6] = alpha[(v / 16) % 4];
        vocab[v][7] = alpha[(v / 4) % 4];
        vocab[v][8] = alpha[v % 4];
        vocab[v][9] = '\0';
    }

    /* Each slot gets its OWN copy, so no lane can shortcut on shared pointers. */
    char **list = malloc(N * sizeof(char *));
    long state = 1;
    for (long i = 0; i < N; i++) {
        state = lcg(state);
        char *copy = malloc(WORD_LEN + 1);
        memcpy(copy, vocab[(state / 65536) % VOCAB_N], WORD_LEN + 1);
        list[i] = copy;
    }

    WordDistance wd;
    wd_build(&wd, list, N);

    long acc = 0;
    long qstate = 7;
    for (long k = 0; k < ITERS; k++) {
        qstate = lcg(qstate);
        long a = (qstate / 65536) % VOCAB_N;
        qstate = lcg(qstate);
        long b = (qstate / 65536) % VOCAB_N;
        if (b == a) b = (b + 1) % VOCAB_N;
        long d = wd_shortest(&wd, vocab[a], vocab[b]);
        acc = (acc * 131 + d) % 1000000007L;
    }
    printf("%ld\n", acc);
    return 0;
}
