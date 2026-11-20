// LeetCode #1206 bench, in C: the ★ arm (a skiplist whose nodes live in
// one array, each node's forward links one per level it stands on, heights
// by coin flips from the list's own generator, erased slots reused) on
// 50000 calls drawn once, a third each of search, add and erase, on values
// up to 20000; then 10 rounds, each on a new list, every answer folded
// into a checksum. A node's links sit in a row of 16, of which it uses its
// height, where the others keep a list of exactly its height.

#include <stdio.h>
#include <stdlib.h>

#define LEVELS 16

typedef struct {
    long long *values;
    long (*next)[LEVELS];
    int *height;
    long len, cap;
    long *free;
    long nfree;
    long long seed;
} Skiplist;

static void list_init(Skiplist *s, long cap) {
    s->values = malloc(cap * sizeof(long long));
    s->next = malloc(cap * sizeof(*s->next));
    s->height = malloc(cap * sizeof(int));
    s->free = malloc(cap * sizeof(long));
    s->cap = cap;
    s->len = 1;
    s->nfree = 0;
    s->seed = 1206;
    s->values[0] = 0;
    s->height[0] = LEVELS;
    for (int l = 0; l < LEVELS; l++) s->next[0][l] = -1;
}

static void list_free(Skiplist *s) {
    free(s->values);
    free(s->next);
    free(s->height);
    free(s->free);
}

static int height(Skiplist *s) {
    int h = 1;
    while (h < LEVELS) {
        s->seed = (s->seed * 1103515245 + 12345) % 2147483648LL;
        if ((s->seed / 65536) % 2 == 1) break;
        h++;
    }
    return h;
}

static void path(const Skiplist *s, long long target, long *out) {
    long x = 0;
    for (int level = LEVELS - 1; level >= 0; level--) {
        while (s->next[x][level] >= 0 && s->values[s->next[x][level]] < target) x = s->next[x][level];
        out[level] = x;
    }
}

static int search(const Skiplist *s, long long target) {
    long p[LEVELS];
    path(s, target, p);
    long at = s->next[p[0]][0];
    return at >= 0 && s->values[at] == target;
}

static void add(Skiplist *s, long long num) {
    long p[LEVELS];
    path(s, num, p);
    int h = height(s);
    long node = s->nfree > 0 ? s->free[--s->nfree] : s->len++;
    s->values[node] = num;
    s->height[node] = h;
    for (int level = 0; level < h; level++) {
        s->next[node][level] = s->next[p[level]][level];
        s->next[p[level]][level] = node;
    }
}

static int erase(Skiplist *s, long long num) {
    long p[LEVELS];
    path(s, num, p);
    long at = s->next[p[0]][0];
    if (at < 0 || s->values[at] != num) return 0;
    for (int level = 0; level < s->height[at]; level++)
        if (s->next[p[level]][level] == at) s->next[p[level]][level] = s->next[at][level];
    s->free[s->nfree++] = at;
    return 1;
}

static long long seed = 1206;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { CALLS = 50000 };
    static long long op[CALLS], val[CALLS];
    for (int k = 0; k < CALLS; k++) {
        op[k] = next_random() % 3;
        long long hi = next_random();
        val[k] = (hi * 32768 + next_random()) % 20001;
    }
    long long check = 0;
    for (int round = 0; round < 10; round++) {
        Skiplist s;
        list_init(&s, CALLS + 1);
        for (int k = 0; k < CALLS; k++) {
            int answer;
            if (op[k] == 0) {
                answer = search(&s, val[k]);
            } else if (op[k] == 1) {
                add(&s, val[k]);
                answer = 1;
            } else {
                answer = erase(&s, val[k]);
            }
            check = (check * 131 + op[k] * 2 + answer) % 1000000007;
        }
        list_free(&s);
    }
    printf("10 rounds of 50000 calls: checksum %lld\n", check);
    return 0;
}
