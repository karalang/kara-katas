// LeetCode #2102: Sequentially Ordinal Rank Tracker -- C mirror of the ★
// arm's benchmark (rank_tracker.kara): the same 20 runs of 4 * 10^4
// calls. Places live in one array; two binary heaps of their indices, the
// served one worst on top and the waiting one best on top; the names
// already drawn sit in an open-addressing hash set.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

enum { ADDS = 20000, SLOTS = 1 << 16 };

typedef struct {
    int64_t score;
    char name[11];
} Place;

static Place places[ADDS];
static int served[ADDS], waiting[ADDS];
static int n_served, n_waiting;
static char seen[SLOTS][11];

// a better than b: a higher score, then the smaller name
static int better(int a, int b) {
    if (places[a].score != places[b].score) return places[a].score > places[b].score;
    return strcmp(places[a].name, places[b].name) < 0;
}

// `top(x, y)`: x belongs above y in the heap
static void push(int *h, int *n, int x, int (*top)(int, int)) {
    int i = (*n)++;
    h[i] = x;
    while (i > 0 && top(h[i], h[(i - 1) / 2])) {
        int p = (i - 1) / 2, t = h[i];
        h[i] = h[p];
        h[p] = t;
        i = p;
    }
}

static int pop(int *h, int *n, int (*top)(int, int)) {
    int x = h[0];
    h[0] = h[--(*n)];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < *n && top(h[l], h[m])) m = l;
        if (r < *n && top(h[r], h[m])) m = r;
        if (m == i) break;
        int t = h[i];
        h[i] = h[m];
        h[m] = t;
        i = m;
    }
    return x;
}

static int worse(int a, int b) { return better(b, a); }

static int64_t seed = 2102;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static int insert_name(const char *name) {
    uint64_t h = 1469598103934665603ull;
    for (const char *c = name; *c; c++) h = (h ^ (unsigned char)*c) * 1099511628211ull;
    for (size_t i = h & (SLOTS - 1);; i = (i + 1) & (SLOTS - 1)) {
        if (seen[i][0] == 0) {
            strcpy(seen[i], name);
            return 1;
        }
        if (strcmp(seen[i], name) == 0) return 0;
    }
}

int main(void) {
    int64_t gets = 0, check = 0;
    for (int r = 0; r < 20; r++) {
        memset(seen, 0, sizeof seen);
        n_served = n_waiting = 0;
        int added = 0, asked = 0;
        while (asked < ADDS) {
            if (added < ADDS && (asked == added || next_random() % 2 == 0)) {
                Place *p = &places[added];
                for (;;) {
                    int64_t len = next_random() % 10 + 1;
                    for (int64_t i = 0; i < len; i++) p->name[i] = (char)('a' + next_random() % 26);
                    p->name[len] = 0;
                    if (insert_name(p->name)) break;
                }
                p->score = wide_random() % 100000 + 1;
                push(served, &n_served, added, worse);
                push(waiting, &n_waiting, pop(served, &n_served, worse), better);
                added++;
            } else {
                int best = pop(waiting, &n_waiting, better);
                push(served, &n_served, best, worse);
                asked++;
                gets++;
                for (const char *c = places[best].name; *c; c++) check = (check * 31 + (unsigned char)*c) % 1000000007;
                check = (check * 31 + 7) % 1000000007;
            }
        }
    }
    printf("20 runs: %lld gets, checksum %lld\n", (long long)gets, (long long)check);
    return 0;
}
