// LeetCode #2157: Groups of Strings -- the benchmark's C mirror of
// groups.kara. C has no map of its own, so each of the two maps is an
// open-addressing table with a separate used flag per slot.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WORDS 5000
#define CAP 131072

typedef struct {
    int64_t keys[CAP];
    int64_t values[CAP];
    char used[CAP];
} Table;

static int64_t slot(const Table *t, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    int64_t i = (int64_t)(h >> 47) & (CAP - 1);
    while (t->used[i] && t->keys[i] != key) {
        i = (i + 1) & (CAP - 1);
    }
    return i;
}

static int64_t seed = 2157;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static void unite(int64_t *parent, int64_t *size, int64_t a, int64_t b) {
    int64_t ra = find(parent, a);
    int64_t rb = find(parent, b);
    if (ra == rb) {
        return;
    }
    int64_t big = ra, small = rb;
    if (size[ra] < size[rb]) {
        big = rb;
        small = ra;
    }
    parent[small] = big;
    size[big] += size[small];
}

static Table first, blanked;

static void group_strings(char words[][9], int64_t n, int64_t *out) {
    static int64_t masks[WORDS], parent[WORDS], size[WORDS];
    memset(first.used, 0, CAP);
    memset(blanked.used, 0, CAP);
    for (int64_t i = 0; i < n; i++) {
        masks[i] = 0;
        for (const char *c = words[i]; *c; c++) {
            masks[i] |= (int64_t)1 << (*c - 'a');
        }
        parent[i] = i;
        size[i] = 1;
    }
    for (int64_t i = 0; i < n; i++) {
        int64_t s = slot(&first, masks[i]);
        if (first.used[s]) {
            unite(parent, size, i, first.values[s]);
        } else {
            first.used[s] = 1;
            first.keys[s] = masks[i];
            first.values[s] = i;
        }
    }
    for (int64_t i = 0; i < n; i++) {
        for (int bit = 0; bit < 26; bit++) {
            if ((masks[i] >> bit) & 1) {
                int64_t less = masks[i] ^ ((int64_t)1 << bit);
                int64_t s = slot(&first, less);
                if (first.used[s]) {
                    unite(parent, size, i, first.values[s]);
                }
                s = slot(&blanked, less);
                if (blanked.used[s]) {
                    unite(parent, size, i, blanked.values[s]);
                } else {
                    blanked.used[s] = 1;
                    blanked.keys[s] = less;
                    blanked.values[s] = i;
                }
            }
        }
    }
    int64_t groups = 0, largest = 0;
    for (int64_t i = 0; i < n; i++) {
        if (find(parent, i) == i) {
            groups++;
            if (size[i] > largest) {
                largest = size[i];
            }
        }
    }
    out[0] = groups;
    out[1] = largest;
}

static void word(char *w) {
    int64_t length = next_random() % 8 + 1;
    int64_t len = 0;
    w[0] = '\0';
    while (len < length) {
        char c = (char)('a' + next_random() % 20);
        if (!strchr(w, c)) {
            w[len++] = c;
            w[len] = '\0';
        }
    }
}

static char lists[4][WORDS][9];

int main(void) {
    for (int l = 0; l < 4; l++) {
        for (int i = 0; i < WORDS; i++) {
            word(lists[l][i]);
        }
    }
    int64_t total = 0, check = 0, answer[2];
    for (int64_t round = 0; round < 25; round++) {
        for (int l = 0; l < 4; l++) {
            int64_t at = next_random() % WORDS;
            word(lists[l][at]);
            group_strings(lists[l], WORDS, answer);
            total += answer[0];
            check = (check * 31 + answer[0] * 10007 + answer[1] + round) % 1000000007;
        }
    }
    printf("100 solves: %lld groups in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
