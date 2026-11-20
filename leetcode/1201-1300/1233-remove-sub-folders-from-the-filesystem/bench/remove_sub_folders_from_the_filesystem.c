// LeetCode #1233 bench: the ★ arm in C, over the same 10 lists of
// 4 · 10^4 folders and 10 passes as the Kāra bench; a repeat is turned
// away by a linear-probing hash table of the folders drawn.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static int cmp(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }

static long remove_subfolders(char **folder, long n, char **sorted) {
    memcpy(sorted, folder, sizeof(char *) * n);
    qsort(sorted, n, sizeof(char *), cmp);
    long kept = 0;
    const char *last = NULL;
    size_t last_len = 0;
    for (long i = 0; i < n; i++) {
        const char *f = sorted[i];
        if (last == NULL || !(strncmp(f, last, last_len) == 0 && f[last_len] == '/')) {
            last = f;
            last_len = strlen(f);
            kept++;
        }
    }
    return kept;
}

static unsigned long hash(const char *s) {
    unsigned long h = 1469598103934665603UL;
    while (*s) h = (h ^ (unsigned char)*s++) * 1099511628211UL;
    return h;
}

int main(void) {
    const char *letters = "abcdefgh";
    long seed = 1233;
    char **lists[10];
    enum { SLOTS = 1 << 17 };
    char **table = malloc(sizeof(char *) * SLOTS);
    for (int l = 0; l < 10; l++) {
        lists[l] = malloc(sizeof(char *) * 40000);
        memset(table, 0, sizeof(char *) * SLOTS);
        long count = 0;
        while (count < 40000) {
            char f[64];
            int len = 0;
            long d = next_random(&seed) % 4 + 1;
            for (long level = 0; level < d; level++) {
                f[len++] = '/';
                for (int k = 0; k < (level == 0 ? 4 : 2); k++) f[len++] = letters[next_random(&seed) % 8];
            }
            f[len] = 0;
            unsigned long h = hash(f) & (SLOTS - 1);
            while (table[h] && strcmp(table[h], f) != 0) h = (h + 1) & (SLOTS - 1);
            if (!table[h]) {
                table[h] = strdup(f);
                lists[l][count++] = table[h];
            }
        }
    }
    char **sorted = malloc(sizeof(char *) * 40000);
    long kept = 0;
    for (int pass = 0; pass < 10; pass++)
        for (int l = 0; l < 10; l++) kept += remove_subfolders(lists[l], 40000, sorted);
    printf("10 lists of 40000 folders, 10 passes: %ld kept\n", kept);
    return 0;
}
