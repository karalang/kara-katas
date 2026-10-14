// Benchmark for #609: the ★ arm (a map from content to paths); see
// find_duplicate.kara. An open-addressing table hashed by FNV-1a, its
// keys copies of the contents as the Kāra arm's are owned strings, each
// value a growable array of "dir/name" copies; the groups of two or more
// go back to the caller, who frees them.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **items;
    int64_t len, cap;
} Group;

typedef struct {
    char *key;
    size_t len;
    Group group;
} Slot;

static char *copy(const char *s, size_t n) {
    char *t = malloc(n + 1);
    memcpy(t, s, n);
    t[n] = 0;
    return t;
}

static uint64_t fnv(const char *s, size_t n) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t k = 0; k < n; k++) {
        h ^= (unsigned char)s[k];
        h *= 1099511628211ULL;
    }
    return h;
}

static void push(Group *g, char *s) {
    if (g->len == g->cap) {
        g->cap = g->cap ? 2 * g->cap : 4;
        g->items = realloc(g->items, (size_t)g->cap * sizeof(char *));
    }
    g->items[g->len++] = s;
}

// Fills `out` with the groups of two or more; returns how many.
static int64_t find_duplicate(char **paths, int64_t n, Group *out) {
    size_t cap = 16, used = 0;
    Slot *table = calloc(cap, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) {
        const char *line = paths[i];
        const char *space = strchr(line, ' ');
        size_t dlen = (size_t)(space - line);
        const char *file = space + 1;
        while (1) {
            const char *end = strchr(file, ' ');
            size_t flen = end ? (size_t)(end - file) : strlen(file);
            const char *open = memchr(file, '(', flen);
            size_t nlen = (size_t)(open - file);
            const char *content = open + 1;
            size_t clen = flen - nlen - 2;
            if (2 * (used + 1) > cap) {
                size_t ncap = 2 * cap;
                Slot *bigger = calloc(ncap, sizeof(Slot));
                for (size_t k = 0; k < cap; k++)
                    if (table[k].key) {
                        size_t h = fnv(table[k].key, table[k].len) & (ncap - 1);
                        while (bigger[h].key) h = (h + 1) & (ncap - 1);
                        bigger[h] = table[k];
                    }
                free(table);
                table = bigger;
                cap = ncap;
            }
            size_t h = fnv(content, clen) & (cap - 1);
            while (table[h].key &&
                   !(table[h].len == clen && memcmp(table[h].key, content, clen) == 0))
                h = (h + 1) & (cap - 1);
            if (!table[h].key) {
                table[h].key = copy(content, clen);
                table[h].len = clen;
                used++;
            }
            char *path = malloc(dlen + 1 + nlen + 1);
            memcpy(path, line, dlen);
            path[dlen] = '/';
            memcpy(path + dlen + 1, file, nlen);
            path[dlen + 1 + nlen] = 0;
            push(&table[h].group, path);
            if (!end) break;
            file = end + 1;
        }
    }
    int64_t size = 0;
    for (size_t k = 0; k < cap; k++) {
        if (!table[k].key) continue;
        free(table[k].key);
        if (table[k].group.len > 1) {
            out[size++] = table[k].group;
        } else {
            for (int64_t j = 0; j < table[k].group.len; j++) free(table[k].group.items[j]);
            free(table[k].group.items);
        }
    }
    free(table);
    return size;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { SYSTEMS = 10, ROUNDS = 300, POOL = 3000, DIRS = 2000 };
    int64_t seed = 609;
    static char *pool[POOL];
    for (int k = 0; k < POOL; k++) {
        int64_t size = 8 + step(&seed) % 13;
        char *c = malloc((size_t)size + 1);
        for (int64_t j = 0; j < size; j++) c[j] = (char)(97 + step(&seed) % 4);
        c[size] = 0;
        pool[k] = c;
    }
    static char *all[SYSTEMS][DIRS];
    for (int s = 0; s < SYSTEMS; s++) {
        int64_t counter = 0;
        for (int d = 0; d < DIRS; d++) {
            char line[512];
            int len = snprintf(line, sizeof line, "root/s%d/d%d", s, d);
            int64_t files = 1 + step(&seed) % 6;
            for (int64_t k = 0; k < files; k++) {
                counter++;
                len += snprintf(line + len, sizeof line - (size_t)len, " f%lld.txt(%s)",
                                (long long)counter, pool[step(&seed) % POOL]);
            }
            all[s][d] = copy(line, (size_t)len);
        }
    }
    static Group found[DIRS * 6];
    int64_t groups = 0, files = 0, checksum = 0;
    for (int r = 0; r < ROUNDS; r++) {
        int64_t size = find_duplicate(all[(r * 3) % SYSTEMS], DIRS, found);
        groups += size;
        for (int64_t g = 0; g < size; g++) {
            files += found[g].len;
            int64_t length = 0;
            for (int64_t j = 0; j < found[g].len; j++) {
                length += (int64_t)strlen(found[g].items[j]);
                free(found[g].items[j]);
            }
            checksum = (checksum + found[g].len * length) % 1000000007;
            free(found[g].items);
        }
    }
    printf("%d systems, %d rounds: %lld groups, %lld files, checksum %lld\n", SYSTEMS, ROUNDS,
           (long long)groups, (long long)files, (long long)checksum);
    return 0;
}
