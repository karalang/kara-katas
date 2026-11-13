// LeetCode #1146: Snapshot Array -- the C mirror of the ★ arm: a history
// of (snap, value) pairs for each place, grown by doubling, the last pair
// at or before the snap asked found by binary search (`partition_point`).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t snap, val; } Pair;
typedef struct { Pair *at; int64_t len, cap; } History;
typedef struct { History *history; int64_t snaps; } SnapshotArray;

static SnapshotArray snapshot_new(int64_t length) {
    SnapshotArray a = { calloc(length, sizeof(History)), 0 };
    for (int64_t i = 0; i < length; i++) {
        a.history[i].at = malloc(sizeof(Pair));
        a.history[i].at[0] = (Pair){ 0, 0 };
        a.history[i].len = a.history[i].cap = 1;
    }
    return a;
}

static void snapshot_set(SnapshotArray *a, int64_t index, int64_t val) {
    History *h = &a->history[index];
    if (h->at[h->len - 1].snap == a->snaps) {
        h->at[h->len - 1].val = val;
        return;
    }
    if (h->len == h->cap) {
        h->cap *= 2;
        h->at = realloc(h->at, h->cap * sizeof(Pair));
    }
    h->at[h->len++] = (Pair){ a->snaps, val };
}

static int64_t snapshot_snap(SnapshotArray *a) { return a->snaps++; }

static int64_t snapshot_get(const SnapshotArray *a, int64_t index, int64_t snap_id) {
    const History *h = &a->history[index];
    int64_t lo = 0, hi = h->len;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (h->at[mid].snap <= snap_id) lo = mid + 1; else hi = mid;
    }
    return h->at[lo - 1].val;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t a = next_random(seed);
    return a * 32768 + next_random(seed);
}

int main(void) {
    int64_t n = 50000;
    SnapshotArray arr = snapshot_new(n);
    int64_t seed = 1146, total = 0, check = 0;
    for (int64_t r = 0; r < 50000; r++) {
        for (int k = 0; k < 50; k++) {
            int64_t i = wide(&seed) % n;
            int64_t v = wide(&seed) % 1000000001;
            snapshot_set(&arr, i, v);
        }
        snapshot_snap(&arr);
        for (int k = 0; k < 50; k++) {
            int64_t i = wide(&seed) % n;
            int64_t s = wide(&seed) % (r + 1);
            int64_t got = snapshot_get(&arr, i, s);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("50000 rounds of 50 sets, a snap and 50 gets on 50000 places: gets total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int64_t i = 0; i < n; i++) free(arr.history[i].at);
    free(arr.history);
    return 0;
}
