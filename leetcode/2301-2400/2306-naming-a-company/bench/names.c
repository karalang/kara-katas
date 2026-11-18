// LeetCode #2306: Naming a Company -- the bench, the ★ arm in C. Group
// the suffixes by first letter, and for each pair of letters multiply the
// suffixes each group does not share with the other, twice. C has no
// set, so each group is an open-addressing hash table of its suffixes,
// keyed by FNV-1a, with the
// order its slots were filled kept for walking it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { LISTS = 10, IDEAS = 50000, WIDTH = 8 };

typedef struct {
    char (*keys)[WIDTH];
    uint8_t *used;
    int64_t *slots; /* the slots in use, in the order they were filled */
    int64_t cap, len;
} Set;

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (uint8_t)*s) * 1099511628211ULL;
    return h;
}

static void set_init(Set *s, int64_t cap) {
    s->cap = cap;
    s->len = 0;
    s->keys = calloc(cap, WIDTH);
    s->used = calloc(cap, 1);
    s->slots = malloc(cap * sizeof(int64_t));
}

static void set_free(Set *s) {
    free(s->keys);
    free(s->used);
    free(s->slots);
}

static int set_contains(const Set *s, const char *key) {
    int64_t i = fnv(key) & (s->cap - 1);
    while (s->used[i]) {
        if (strcmp(s->keys[i], key) == 0) return 1;
        i = (i + 1) & (s->cap - 1);
    }
    return 0;
}

static int set_insert(Set *s, const char *key) {
    int64_t i = fnv(key) & (s->cap - 1);
    while (s->used[i]) {
        if (strcmp(s->keys[i], key) == 0) return 0;
        i = (i + 1) & (s->cap - 1);
    }
    s->used[i] = 1;
    strcpy(s->keys[i], key);
    s->slots[s->len++] = i;
    return 1;
}

static int64_t distinct_names(char ideas[][WIDTH], int64_t n) {
    Set groups[26];
    for (int a = 0; a < 26; a++) set_init(&groups[a], 1 << 13);
    for (int64_t i = 0; i < n; i++) set_insert(&groups[ideas[i][0] - 'a'], ideas[i] + 1);
    int64_t names = 0;
    for (int a = 0; a < 26; a++)
        for (int b = a + 1; b < 26; b++) {
            int64_t shared = 0;
            for (int64_t i = 0; i < groups[a].len; i++)
                if (set_contains(&groups[b], groups[a].keys[groups[a].slots[i]])) shared++;
            names += 2 * (groups[a].len - shared) * (groups[b].len - shared);
        }
    for (int a = 0; a < 26; a++) set_free(&groups[a]);
    return names;
}

static int64_t seed = 2306;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char lists[LISTS][IDEAS][WIDTH];
    for (int a = 0; a < LISTS; a++) {
        Set seen;
        set_init(&seen, 1 << 17);
        int64_t count = 0;
        while (count < IDEAS) {
            char idea[WIDTH] = {0};
            int len = 0;
            idea[len++] = 'a' + next_random() % 26;
            int64_t more = next_random() % 7;
            for (int64_t m = 0; m < more; m++) idea[len++] = 'a' + next_random() % 6;
            if (set_insert(&seen, idea)) strcpy(lists[a][count++], idea);
        }
        set_free(&seen);
    }
    int64_t check = 0;
    for (int p = 0; p < 4; p++)
        for (int a = 0; a < LISTS; a++) check = (check * 31 + distinct_names(lists[a], IDEAS)) % 1000000007;
    printf("4 passes over 10 lists of 5 * 10^4 ideas: checksum %lld\n", (long long)check);
    return 0;
}
