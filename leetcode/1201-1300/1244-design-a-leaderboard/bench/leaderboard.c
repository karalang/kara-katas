// LeetCode #1244 bench, in C: the ★ arm (each player's total in a hash
// table, open addressing with linear probing and tombstones for resets,
// cleared per session; a top sorts the totals from the highest with qsort
// and adds the first k) on 100 sessions of 3000 random calls on players up
// to 10000; the tops' answers folded into a checksum.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 16384
#define EMPTY 0
#define USED 1
#define GONE 2

static long long keys[SLOTS], vals[SLOTS];
static char state[SLOTS];
static long long all[SLOTS];

static unsigned slot_of(long long k) {
    unsigned long long h = (unsigned long long)k * 0x9E3779B97F4A7C15ULL;
    return (unsigned)(h >> 50);
}

static long long *find(long long k) {
    unsigned s = slot_of(k);
    while (state[s] != EMPTY) {
        if (state[s] == USED && keys[s] == k) return &vals[s];
        s = (s + 1) & (SLOTS - 1);
    }
    return NULL;
}

static void add_score(long long player, long long score) {
    long long *v = find(player);
    if (v) {
        *v += score;
        return;
    }
    unsigned s = slot_of(player);
    while (state[s] == USED) s = (s + 1) & (SLOTS - 1);
    state[s] = USED;
    keys[s] = player;
    vals[s] = score;
}

static int descending(const void *a, const void *b) {
    long long x = *(const long long *)a, y = *(const long long *)b;
    return (y > x) - (y < x);
}

static long long top(long long k) {
    int n = 0;
    for (int s = 0; s < SLOTS; s++)
        if (state[s] == USED) all[n++] = vals[s];
    qsort(all, n, sizeof all[0], descending);
    long long sum = 0;
    for (long long i = 0; i < k; i++) sum += all[i];
    return sum;
}

static void reset(long long player) {
    unsigned s = slot_of(player);
    while (state[s] != EMPTY) {
        if (state[s] == USED && keys[s] == player) {
            state[s] = GONE;
            return;
        }
        s = (s + 1) & (SLOTS - 1);
    }
}

static long long seed = 1244;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long on[SLOTS];

static void session(long long calls, long long players, long long *tops_out, long long *check_out) {
    memset(state, 0, sizeof state);
    int n = 0;
    long long check = 0, tops = 0;
    for (long long c = 0; c < calls; c++) {
        long long op = next_random() % 4;
        if (op <= 1 || n == 0) {
            long long player = next_random() % players + 1;
            long long score = next_random() % 100 + 1;
            add_score(player, score);
            int seen = 0;
            for (int i = 0; i < n; i++)
                if (on[i] == player) {
                    seen = 1;
                    break;
                }
            if (!seen) on[n++] = player;
        } else if (op == 2) {
            long long got = top(next_random() % n + 1);
            check = (check * 131 + got) % 1000000007;
            tops++;
        } else {
            int i = (int)(next_random() % n);
            long long player = on[i];
            on[i] = on[--n];
            reset(player);
        }
    }
    *tops_out = tops;
    *check_out = check;
}

int main(void) {
    long long tops = 0, check = 0;
    for (int s = 0; s < 100; s++) {
        long long t, c;
        session(3000, 10000, &t, &c);
        tops += t;
        check = (check * 31 + c) % 1000000007;
    }
    printf("100 sessions of 3000 calls on 10000 players: %lld tops, checksum %lld\n", tops, check);
    return 0;
}
