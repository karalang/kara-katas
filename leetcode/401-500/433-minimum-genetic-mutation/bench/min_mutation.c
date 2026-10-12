// Benchmark for #433: mirror of min_mutation.kara (breadth first,
// generating neighbours). The set of unreached genes is an
// open-addressing table of 8-letter strings hashed with FNV-1a, with
// tombstones for removal, rebuilt from the bank for every search as the
// Kāra arm builds its Set; mutants are built as strings, as there.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 4096

typedef struct { char gene[9]; int state; } Slot;  // 0 empty, 1 full, 2 removed

static uint64_t fnv(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static void insert(Slot *t, const char *g) {
    uint64_t i = fnv(g) & (SLOTS - 1);
    int64_t free_at = -1;
    while (t[i].state != 0) {
        if (t[i].state == 1 && strcmp(t[i].gene, g) == 0) return;
        if (t[i].state == 2 && free_at < 0) free_at = i;
        i = (i + 1) & (SLOTS - 1);
    }
    if (free_at >= 0) i = free_at;
    strcpy(t[i].gene, g);
    t[i].state = 1;
}

static int64_t find(Slot *t, const char *g) {
    uint64_t i = fnv(g) & (SLOTS - 1);
    while (t[i].state != 0) {
        if (t[i].state == 1 && strcmp(t[i].gene, g) == 0) return i;
        i = (i + 1) & (SLOTS - 1);
    }
    return -1;
}

static int take(Slot *t, const char *g) {
    int64_t i = find(t, g);
    if (i < 0) return 0;
    t[i].state = 2;
    return 1;
}

static int64_t min_mutation(const char *start, const char *end, char (*bank)[9], int64_t n, Slot *t, char (*level)[9], char (*next)[9]) {
    memset(t, 0, SLOTS * sizeof *t);
    for (int64_t i = 0; i < n; i++) insert(t, bank[i]);
    if (find(t, end) < 0) return -1;
    take(t, start);
    int64_t len = 1, steps = 0;
    strcpy(level[0], start);
    static const char letters[4] = {'A', 'C', 'G', 'T'};
    while (len > 0) {
        int64_t nlen = 0;
        for (int64_t k = 0; k < len; k++) {
            if (strcmp(level[k], end) == 0) return steps;
            for (int i = 0; i < 8; i++) {
                for (int c = 0; c < 4; c++) {
                    if (letters[c] != level[k][i]) {
                        char mutant[9];
                        memcpy(mutant, level[k], 9);
                        mutant[i] = letters[c];
                        if (take(t, mutant)) strcpy(next[nlen++], mutant);
                    }
                }
            }
        }
        memcpy(level, next, nlen * sizeof *next);
        len = nlen;
        steps++;
    }
    return -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static void mutate(const char *gene, char *out, int64_t *seed) {
    static const char letters[4] = {'A', 'C', 'G', 'T'};
    int64_t at = next_random(seed) % 8;
    int64_t shift = 1 + next_random(seed) % 3;
    for (int i = 0; i < 8; i++) {
        if (i == at) {
            int k = gene[i] == 'A' ? 0 : gene[i] == 'C' ? 1 : gene[i] == 'G' ? 2 : 3;
            out[i] = letters[(k + shift) % 4];
        } else {
            out[i] = gene[i];
        }
    }
    out[8] = 0;
}

int main(int argc, char **argv) {
    int64_t size = 1000;
    int64_t searches = argc > 1 ? atoll(argv[1]) : 2000;
    int64_t seed = 433;
    char (*bank)[9] = malloc(size * sizeof *bank);
    strcpy(bank[0], "ACGTACGT");
    for (int64_t n = 1; n < size; n++) {
        int64_t parent = next_random(&seed) % n;
        mutate(bank[parent], bank[n], &seed);
    }
    Slot *t = malloc(SLOTS * sizeof *t);
    char (*level)[9] = malloc((size + 1) * sizeof *level);
    char (*next)[9] = malloc((size + 1) * sizeof *next);
    int64_t reachable = 0, checksum = 0;
    for (int64_t s = 0; s < searches; s++) {
        char start[9];
        mutate(bank[next_random(&seed) % size], start, &seed);
        const char *end = bank[next_random(&seed) % size];
        int64_t answer = min_mutation(start, end, bank, size, t, level, next);
        if (answer >= 0) reachable++;
        checksum = (checksum * 31 + answer + 2) % 1000000007;
    }
    printf("%lld searches in a bank of %lld: %lld reachable, checksum %lld\n", (long long)searches, (long long)size, (long long)reachable, (long long)checksum);
    return 0;
}
