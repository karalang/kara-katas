// Benchmark workload for LeetCode #249 — Group Shifted Strings (C mirror).
// Mirrors group_shifted.kara algorithm-for-algorithm. C has no string map, so
// one is provided: open addressing with linear probing, FNV-1a hash, and a
// growable char* list per slot -- the closest structural analogue to
// Map[String, Vec[String]] with in-place append.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char **items; long len, cap; } StrVec;
static void sv_push(StrVec *v, const char *s) {
    if (v->len == v->cap) { v->cap = v->cap ? v->cap * 2 : 4; v->items = realloc(v->items, v->cap * sizeof(char *)); }
    v->items[v->len++] = strdup(s);
}
static void sv_free(StrVec *v) { for (long i = 0; i < v->len; i++) free(v->items[i]); free(v->items); }

typedef struct { char *key; StrVec vals; int used; } Slot;
typedef struct { Slot *slots; long cap, len; } Map;

static unsigned long fnv1a(const char *s) {
    unsigned long h = 1469598103934665603UL;
    for (const unsigned char *p = (const unsigned char *)s; *p; p++) { h ^= *p; h *= 1099511628211UL; }
    return h;
}
static void map_init(Map *m, long cap) { m->cap = cap; m->len = 0; m->slots = calloc(cap, sizeof(Slot)); }
static void map_free(Map *m) {
    for (long i = 0; i < m->cap; i++) if (m->slots[i].used) { free(m->slots[i].key); sv_free(&m->slots[i].vals); }
    free(m->slots);
}
static long map_find(Map *m, const char *key) {   // slot index; used==0 means absent
    long i = (long)(fnv1a(key) & (unsigned long)(m->cap - 1));
    while (m->slots[i].used && strcmp(m->slots[i].key, key) != 0) i = (i + 1) & (m->cap - 1);
    return i;
}
static void map_grow(Map *m) {
    Map n; map_init(&n, m->cap * 2);
    for (long i = 0; i < m->cap; i++) if (m->slots[i].used) {
        long j = map_find(&n, m->slots[i].key);
        n.slots[j].used = 1; n.slots[j].key = m->slots[i].key; n.slots[j].vals = m->slots[i].vals; n.len++;
    }
    free(m->slots); *m = n;
}

static char *canonical(const char *word) {
    long n = (long)strlen(word);
    if (n == 0) return strdup("");
    long shift = (long)(unsigned char)word[0] - 'a';
    char *out = malloc(n * 4 + 1);
    long o = 0;
    for (long i = 0; i < n; i++) {
        long c = (((long)(unsigned char)word[i] - 'a' - shift) + 26) % 26;
        o += sprintf(out + o, "%ld,", c);
    }
    out[o] = '\0';
    return out;
}

int main(void) {
    long words_n = 120000, rounds = 5;

    char **words = malloc(words_n * sizeof(char *));
    long state = 249249;
    for (long w = 0; w < words_n; w++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long len = (state / 65536L) % 10L + 3L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long seed = (state / 65536L) % 40L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long shift = (state / 65536L) % 26L;

        char *s = malloc(len + 1);
        for (long i = 0; i < len; i++) {
            long base = (seed * 7 + i * 11) % 26;
            s[i] = (char)(97 + (base + shift) % 26);
        }
        s[len] = '\0';
        words[w] = s;
    }

    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        Map t; map_init(&t, 1 << 16);
        long groups = 0, keysum = 0;
        for (long i = 0; i < words_n; i++) {
            char *key = canonical(words[i]);
            for (const unsigned char *p = (const unsigned char *)key; *p; p++)
                keysum = (keysum * 31 + (long)*p) % 1000000007L;
            if (t.len * 10 >= t.cap * 7) map_grow(&t);
            long j = map_find(&t, key);
            if (!t.slots[j].used) {
                groups++;
                t.slots[j].used = 1;
                t.slots[j].key = strdup(key);
                t.slots[j].vals = (StrVec){0, 0, 0};
                t.len++;
            }
            sv_push(&t.slots[j].vals, words[i]);
            free(key);
        }
        sink = (sink * 131 + groups) % 1000000007L;
        sink = (sink * 31 + keysum) % 1000000007L;
        map_free(&t);
    }
    printf("%ld\n", sink);
    for (long w = 0; w < words_n; w++) free(words[w]);
    free(words);
    return 0;
}
