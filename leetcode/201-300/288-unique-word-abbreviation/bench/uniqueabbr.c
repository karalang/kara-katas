/* Benchmark twin for LeetCode #288 — same algorithm as uniqueabbr.kara.
 *
 * C has no hash map in its standard library, so one is spelled out here: open
 * addressing with linear probing, FNV-1a over the key bytes. The SLOT is the
 * Kara `Bucket` enum by another name — an empty slot is the map's absence, a
 * slot with conflicted==0 is `Sole(word)`, and conflicted==1 is `Conflicted`.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define DICT_N   3000
#define POOL_N   20000
#define PUNCHES  1000000
#define TABLE_SZ 16384          /* power of two, > 2x the distinct abbreviations */
#define MAXW     16

static const char *LETTERS = "abcdefghijklmnopqrstuvwxyz";

typedef struct {
    char key[MAXW];             /* abbreviation; empty means a free slot */
    char word[MAXW];            /* the sole word, when conflicted == 0 */
    int  used;
    int  conflicted;
} slot;

static slot table[TABLE_SZ];

static uint64_t fnv1a(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    while (*s) {
        h ^= (unsigned char)*s++;
        h *= 1099511628211ULL;
    }
    return h;
}

/* Returns the slot for `key`, inserting an empty one if absent. */
static slot *slot_for(const char *key) {
    size_t i = (size_t)(fnv1a(key) & (TABLE_SZ - 1));
    for (;;) {
        if (!table[i].used) {
            table[i].used = 1;
            strcpy(table[i].key, key);
            return &table[i];
        }
        if (strcmp(table[i].key, key) == 0) return &table[i];
        i = (i + 1) & (TABLE_SZ - 1);
    }
}

/* Read-only probe: NULL when the abbreviation is absent. */
static slot *slot_find(const char *key) {
    size_t i = (size_t)(fnv1a(key) & (TABLE_SZ - 1));
    for (;;) {
        if (!table[i].used) return NULL;
        if (strcmp(table[i].key, key) == 0) return &table[i];
        i = (i + 1) & (TABLE_SZ - 1);
    }
}

static void abbrev(const char *w, char *out) {
    size_t n = strlen(w);
    if (n <= 2) { strcpy(out, w); return; }
    sprintf(out, "%c%zu%c", w[0], n - 2, w[n - 1]);
}

static int64_t next_rand(int64_t state) {
    return (state * 1103515245 + 12345) & 2147483647;
}

int main(void) {
    static char dict[DICT_N][MAXW];
    static char pool[POOL_N][MAXW];
    int64_t seed = 12345;
    char a[MAXW];

    for (int i = 0; i < DICT_N; i++) {
        seed = next_rand(seed);
        int64_t n = 3 + ((seed / 65536) % 8);
        for (int64_t j = 0; j < n; j++) {
            seed = next_rand(seed);
            dict[i][j] = LETTERS[(seed / 65536) % 26];
        }
        dict[i][n] = '\0';
    }

    for (int i = 0; i < DICT_N; i++) {
        abbrev(dict[i], a);
        slot *s = slot_for(a);
        if (s->word[0] == '\0' && !s->conflicted) {
            strcpy(s->word, dict[i]);                 /* -> Sole(word) */
        } else if (!s->conflicted && strcmp(s->word, dict[i]) != 0) {
            s->conflicted = 1;                        /* -> Conflicted */
            s->word[0] = '\0';
        }
    }

    for (int i = 0; i < POOL_N; i++) {
        if (i % 2 == 0) {
            strcpy(pool[i], dict[(i * 7) % DICT_N]);
        } else {
            seed = next_rand(seed);
            int64_t n = 3 + ((seed / 65536) % 8);
            for (int64_t j = 0; j < n; j++) {
                seed = next_rand(seed);
                pool[i][j] = LETTERS[(seed / 65536) % 26];
            }
            pool[i][n] = '\0';
        }
    }

    int64_t unique_count = 0;
    for (int64_t i = 0; i < PUNCHES; i++) {
        const char *word = pool[i % POOL_N];
        abbrev(word, a);
        slot *s = slot_find(a);
        int u;
        if (s == NULL)          u = 1;
        else if (s->conflicted) u = 0;
        else                    u = strcmp(s->word, word) == 0;
        if (u) unique_count++;
    }
    printf("unique %lld\n", (long long)unique_count);
    return 0;
}
