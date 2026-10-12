// Benchmark for #432: mirror of all_one.kara (a list of count buckets).
// The key-to-bucket map is an open-addressing table hashing the key
// text with FNV-1a; a key's entry stays in the table once made, with no
// bucket while its count is 0. A bucket's set of keys is an array of
// entries, each entry knowing its position, so a key leaves its bucket
// by a swap with the last one, in O(1) like the Kāra arm's Set.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Bucket;

typedef struct {
    char key[16];
    struct Bucket *bucket;
    int64_t pos;
    int used;
} Entry;

typedef struct Bucket {
    int64_t count;
    Entry **keys;
    int64_t len, cap;
    struct Bucket *prev, *next;
} Bucket;

#define SLOTS 32768

typedef struct {
    Bucket *head, *tail;
    Entry *table;
} AllOne;

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static Entry *entry(AllOne *ds, const char *key, int make) {
    uint64_t i = fnv(key) & (SLOTS - 1);
    while (ds->table[i].used) {
        if (strcmp(ds->table[i].key, key) == 0) return &ds->table[i];
        i = (i + 1) & (SLOTS - 1);
    }
    if (!make) return NULL;
    Entry *e = &ds->table[i];
    e->used = 1;
    strcpy(e->key, key);
    e->bucket = NULL;
    return e;
}

static Bucket *bucket(int64_t count) {
    Bucket *b = calloc(1, sizeof *b);
    b->count = count;
    return b;
}

static void add(Bucket *b, Entry *e) {
    if (b->len == b->cap) {
        b->cap = b->cap ? b->cap * 2 : 4;
        b->keys = realloc(b->keys, b->cap * sizeof *b->keys);
    }
    e->pos = b->len;
    b->keys[b->len++] = e;
    e->bucket = b;
}

static void take(Bucket *b, Entry *e) {
    Entry *last = b->keys[--b->len];
    b->keys[e->pos] = last;
    last->pos = e->pos;
}

static Bucket *link_after(Bucket *at, int64_t count) {
    Bucket *b = bucket(count);
    Bucket *after = at->next;
    b->next = after;
    after->prev = b;
    at->next = b;
    b->prev = at;
    return b;
}

static void drop_if_empty(Bucket *b) {
    if (b->len > 0) return;
    b->prev->next = b->next;
    b->next->prev = b->prev;
    free(b->keys);
    free(b);
}

static AllOne all_one_new(void) {
    AllOne ds;
    ds.head = bucket(0);
    ds.tail = bucket(-1);
    ds.head->next = ds.tail;
    ds.tail->prev = ds.head;
    ds.table = calloc(SLOTS, sizeof *ds.table);
    return ds;
}

static void inc(AllOne *ds, const char *key) {
    Entry *e = entry(ds, key, 1);
    Bucket *cur = e->bucket ? e->bucket : ds->head;
    Bucket *after = cur->next;
    Bucket *up = after->count == cur->count + 1 ? after : link_after(cur, cur->count + 1);
    if (cur != ds->head) take(cur, e);
    add(up, e);
    if (cur != ds->head) drop_if_empty(cur);
}

static void dec(AllOne *ds, const char *key) {
    Entry *e = entry(ds, key, 0);
    Bucket *cur = e->bucket;
    take(cur, e);
    if (cur->count == 1) {
        e->bucket = NULL;
    } else {
        Bucket *before = cur->prev;
        Bucket *down = before->count == cur->count - 1 ? before : link_after(before, cur->count - 1);
        add(down, e);
    }
    drop_if_empty(cur);
}

static const char *any_key(Bucket *b) {
    return b->len > 0 ? b->keys[0]->key : "";
}

static const char *get_max_key(AllOne *ds) { return any_key(ds->tail->prev); }
static const char *get_min_key(AllOne *ds) { return any_key(ds->head->next); }

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t key_id(const char *key) {
    if (!*key) return -1;
    int64_t id = 0;
    for (const char *p = key; *p; p++)
        if (*p != 'k') id = id * 10 + (*p - '0');
    return id;
}

int main(int argc, char **argv) {
    int64_t keys = 10000;
    int64_t operations = argc > 1 ? atoll(argv[1]) : 2000000;
    int64_t seed = 432;
    AllOne ds = all_one_new();
    int64_t *count = calloc(keys, sizeof *count);
    int64_t queries = 0, checksum = 0;
    char key[16];
    for (int64_t i = 0; i < operations; i++) {
        int64_t roll = next_random(&seed) % 10;
        int64_t hi = next_random(&seed);
        int64_t id = (hi * 32768 + next_random(&seed)) % keys;
        if (roll < 2) {
            int64_t a = key_id(roll == 0 ? get_max_key(&ds) : get_min_key(&ds));
            int64_t c = a < 0 ? 0 : count[a];
            queries++;
            checksum = (checksum * 31 + c + 1) % 1000000007;
        } else if (roll < 5 && count[id] > 0) {
            snprintf(key, sizeof key, "k%lld", (long long)id);
            dec(&ds, key);
            count[id]--;
        } else {
            snprintf(key, sizeof key, "k%lld", (long long)id);
            inc(&ds, key);
            count[id]++;
        }
    }
    printf("%lld operations on %lld keys: %lld queries, checksum %lld\n", (long long)operations, (long long)keys, (long long)queries, (long long)checksum);
    return 0;
}
