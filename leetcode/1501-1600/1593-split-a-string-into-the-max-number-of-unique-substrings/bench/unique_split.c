// LeetCode #1593: Split a String Into the Max Number of Unique Substrings
// -- the bench in C, mirroring unique_split.kara. C has no set: the
// pieces used are kept in an open-addressing table of owned copies,
// hashed by FNV-1a, with linear probing and backward-shift removal; each
// piece is copied into a malloc as Kāra's `to_string` does.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP 64
typedef struct {
    char *keys[CAP];
    uint8_t full[CAP];
    int len;
} Set;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (uint8_t)*s) * 1099511628211ULL;
    return h;
}

static int find(Set *t, const char *k) {
    for (uint64_t i = hash(k) & (CAP - 1);; i = (i + 1) & (CAP - 1)) {
        if (!t->full[i]) return -1;
        if (strcmp(t->keys[i], k) == 0) return (int)i;
    }
}

static void insert(Set *t, char *k) {
    uint64_t i = hash(k) & (CAP - 1);
    while (t->full[i]) i = (i + 1) & (CAP - 1);
    t->keys[i] = k;
    t->full[i] = 1;
    t->len++;
}

// the slot emptied, and each later key in its run moved back into the
// gap when its home slot is not between the gap and itself
static void erase(Set *t, int i) {
    free(t->keys[i]);
    t->full[i] = 0;
    t->len--;
    for (int j = (i + 1) & (CAP - 1); t->full[j]; j = (j + 1) & (CAP - 1)) {
        int home = (int)(hash(t->keys[j]) & (CAP - 1));
        if (((j - home) & (CAP - 1)) >= ((j - i) & (CAP - 1))) {
            t->keys[i] = t->keys[j];
            t->full[i] = 1;
            t->full[j] = 0;
            i = j;
        }
    }
}

static void split_from(const char *s, int n, int at, Set *used, int *best) {
    if (at == n) {
        if (used->len > *best) *best = used->len;
        return;
    }
    if (used->len + (n - at) <= *best) return;
    for (int end = at + 1; end <= n; end++) {
        char *piece = malloc(end - at + 1);
        memcpy(piece, s + at, end - at);
        piece[end - at] = 0;
        if (find(used, piece) < 0) {
            insert(used, piece);
            split_from(s, n, end, used, best);
            erase(used, find(used, piece));
        } else {
            free(piece);
        }
    }
}

static int max_unique_split(const char *s, int n) {
    Set *used = calloc(1, sizeof(Set));
    int best = 0;
    split_from(s, n, 0, used, &best);
    free(used);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1593;
    char (*strings)[17] = malloc(20000 * sizeof *strings);
    for (int k = 0; k < 20000; k++) {
        for (int i = 0; i < 16; i++) strings[k][i] = (char)('a' + next_random(&seed) % 3);
        strings[k][16] = 0;
    }
    int64_t check = 0, total = 0;
    for (int k = 0; k < 20000; k++) {
        int64_t answer = max_unique_split(strings[k], 16);
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("20000 strings of 16 letters: total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
