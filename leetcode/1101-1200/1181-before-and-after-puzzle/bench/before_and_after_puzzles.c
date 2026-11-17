// LeetCode #1181: Before and After Puzzle -- the ★ arm in C: the phrases'
// indices grouped by first word in an open-addressing hash table, each
// phrase's last word looking up the phrases that start with it, the
// puzzles gathered in an array, sorted and their repeats dropped (C has no
// ordered set).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 256

typedef struct {
    const char *word;
    int len;
    int count;
    int idx[100];
} Slot;

static uint64_t hash(const char *s, int n) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < n; i++) h = (h ^ (unsigned char)s[i]) * 1099511628211ULL;
    return h;
}

static Slot *find(Slot *t, const char *w, int n, int insert) {
    for (uint64_t k = hash(w, n) % SLOTS;; k = (k + 1) % SLOTS) {
        if (t[k].word == NULL) {
            if (!insert) return NULL;
            t[k].word = w;
            t[k].len = n;
            t[k].count = 0;
            return &t[k];
        }
        if (t[k].len == n && memcmp(t[k].word, w, n) == 0) return &t[k];
    }
}

static int cmp(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }

// The puzzles, sorted and each once; returns how many, `*out` owned by the caller.
static int before_and_after_puzzles(char **phrases, int n, char ***out) {
    static Slot table[SLOTS];
    memset(table, 0, sizeof table);
    for (int i = 0; i < n; i++) {
        const char *sp = strchr(phrases[i], ' ');
        int len = sp ? (int)(sp - phrases[i]) : (int)strlen(phrases[i]);
        Slot *s = find(table, phrases[i], len, 1);
        s->idx[s->count++] = i;
    }
    int cap = 1024, k = 0;
    char **puzzles = malloc(cap * sizeof *puzzles);
    for (int i = 0; i < n; i++) {
        const char *p = phrases[i];
        int plen = (int)strlen(p);
        const char *sp = strrchr(p, ' ');
        const char *last = sp ? sp + 1 : p;
        Slot *s = find(table, last, (int)(p + plen - last), 0);
        if (!s) continue;
        for (int c = 0; c < s->count; c++) {
            int j = s->idx[c];
            if (j == i) continue;
            const char *rest = strchr(phrases[j], ' ');
            if (!rest) rest = "";
            int rlen = (int)strlen(rest);
            char *q = malloc(plen + rlen + 1);
            memcpy(q, p, plen);
            memcpy(q + plen, rest, rlen + 1);
            if (k == cap) puzzles = realloc(puzzles, (cap *= 2) * sizeof *puzzles);
            puzzles[k++] = q;
        }
    }
    qsort(puzzles, k, sizeof *puzzles, cmp);
    int m = 0;
    for (int i = 0; i < k; i++) {
        if (m > 0 && strcmp(puzzles[m - 1], puzzles[i]) == 0) {
            free(puzzles[i]);
        } else {
            puzzles[m++] = puzzles[i];
        }
    }
    *out = puzzles;
    return m;
}

static int64_t seed = 1181;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static const char *vocabulary[] = {"a", "be", "cat", "dog", "eel", "fig", "go", "hat"};
    static char *problems[100][100];
    for (int t = 0; t < 100; t++) {
        int64_t m = 2 + next_random() % 7;
        for (int k = 0; k < 100; k++) {
            int64_t n = 1 + next_random() % 25;
            char buf[128];
            int len = 0;
            for (int64_t w = 0; w < n; w++) {
                const char *v = vocabulary[next_random() % m];
                if (w > 0) buf[len++] = ' ';
                int vl = (int)strlen(v);
                memcpy(buf + len, v, vl);
                len += vl;
            }
            buf[len] = 0;
            problems[t][k] = strdup(buf);
        }
    }
    int rounds = 5;
    int64_t check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int t = 0; t < 100; t++) {
            char **puzzles;
            int count = before_and_after_puzzles(problems[t], 100, &puzzles);
            check = (check * 131 + count) % 1000000007;
            for (int i = 0; i < count; i++) {
                check = (check * 31 + (int64_t)strlen(puzzles[i])) % 1000000007;
                free(puzzles[i]);
            }
            free(puzzles);
        }
    }
    printf("%d rounds of 100 problems: checksum %lld\n", rounds, (long long)check);
    return 0;
}
