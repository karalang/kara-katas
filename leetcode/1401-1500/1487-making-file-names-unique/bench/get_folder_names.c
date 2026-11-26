// LeetCode #1487: Making File Names Unique -- bench, the C twin of
// get_folder_names.kara. C has no map: names are kept in an
// open-addressing table keyed by an FNV-1a hash, grown at half full.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 50000
#define LEN 48

typedef struct {
    char key[LEN];
    int64_t value;
    int used;
} Slot;

typedef struct {
    Slot *slots;
    size_t cap, count;
} Table;

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static Slot *find(Table *t, const char *key) {
    size_t i = fnv(key) & (t->cap - 1);
    while (t->slots[i].used && strcmp(t->slots[i].key, key) != 0) i = (i + 1) & (t->cap - 1);
    return &t->slots[i];
}

static void put(Table *t, const char *key, int64_t value);

static void grow(Table *t) {
    Slot *old = t->slots;
    size_t cap = t->cap;
    t->cap *= 2;
    t->slots = calloc(t->cap, sizeof(Slot));
    t->count = 0;
    for (size_t i = 0; i < cap; i++)
        if (old[i].used) put(t, old[i].key, old[i].value);
    free(old);
}

static void put(Table *t, const char *key, int64_t value) {
    if ((t->count + 1) * 2 > t->cap) grow(t);
    Slot *s = find(t, key);
    if (!s->used) {
        s->used = 1;
        strcpy(s->key, key);
        t->count++;
    }
    s->value = value;
}

static void get_folder_names(char names[][LEN], int n, char out[][LEN]) {
    Table t = {calloc(1024, sizeof(Slot)), 1024, 0};
    char made[LEN];
    for (int i = 0; i < n; i++) {
        Slot *s = find(&t, names[i]);
        if (!s->used) {
            put(&t, names[i], 1);
            strcpy(out[i], names[i]);
            continue;
        }
        int64_t k = s->value;
        for (;;) {
            snprintf(made, LEN, "%s(%lld)", names[i], (long long)k);
            if (!find(&t, made)->used) break;
            k++;
        }
        put(&t, names[i], k + 1);
        put(&t, made, 1);
        strcpy(out[i], made);
    }
    free(t.slots);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void name_of(char *dst, int64_t b, int64_t suffix) {
    if (suffix == 0) snprintf(dst, LEN, "%c%lld", (char)('a' + b % 26), (long long)(b / 26));
    else snprintf(dst, LEN, "%c%lld(%lld)", (char)('a' + b % 26), (long long)(b / 26), (long long)suffix);
}

static char names[N][LEN];
static char folders[N][LEN];

int main(void) {
    int64_t seed = 1487;
    for (int i = 0; i < N; i++) {
        int64_t b = next_random(&seed) % 3000;
        int64_t s = next_random(&seed) % 9;
        name_of(names[i], b, s < 3 ? s + 1 : 0);
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 20; pass++) {
        name_of(names[check % N], check % 3000, check % 4);
        get_folder_names(names, N, folders);
        for (int i = 0; i < N; i++)
            for (const char *p = folders[i]; *p; p++) check = (check * 131 + (unsigned char)*p) % 1000000007;
        check = (check + pass) % 1000000007;
    }
    printf("20 passes over 50000 names: checksum %lld\n", (long long)check);
    return 0;
}
