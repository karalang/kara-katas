// Benchmark for #582: C mirror of the ★ arm (children lists, walked
// breadth first); see kill_process.kara. C has no hash map, so each call
// makes a fresh open-addressing table from parent to a growable array of
// children (131,072 slots, hashed by a 64-bit multiply), walks it with an
// array used as the queue, and frees it all.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 131072

typedef struct {
    int64_t key;
    int used;
    int64_t *items;
    int64_t len, cap;
} Slot;

static Slot *find(Slot *table, int64_t key) {
    uint64_t h = ((uint64_t)key * 0x9E3779B97F4A7C15ull) >> 47;
    while (table[h].used && table[h].key != key) {
        h = (h + 1) & (SLOTS - 1);
    }
    return &table[h];
}

static int64_t *kill_process(const int64_t *pid, const int64_t *ppid, int64_t n, int64_t kill, int64_t *out_len) {
    Slot *children = calloc(SLOTS, sizeof(Slot));
    for (int64_t i = 0; i < n; i++) {
        Slot *s = find(children, ppid[i]);
        if (!s->used) {
            s->used = 1;
            s->key = ppid[i];
        }
        if (s->len == s->cap) {
            s->cap = s->cap ? s->cap * 2 : 4;
            s->items = realloc(s->items, s->cap * sizeof(int64_t));
        }
        s->items[s->len++] = pid[i];
    }
    int64_t *killed = malloc(n * sizeof(int64_t));
    int64_t *queue = malloc(n * sizeof(int64_t));
    int64_t head = 0, tail = 0, len = 0;
    queue[tail++] = kill;
    while (head < tail) {
        int64_t p = queue[head++];
        killed[len++] = p;
        Slot *s = find(children, p);
        if (s->used) {
            for (int64_t k = 0; k < s->len; k++) {
                queue[tail++] = s->items[k];
            }
        }
    }
    for (int64_t h = 0; h < SLOTS; h++) {
        free(children[h].items);
    }
    free(children);
    free(queue);
    *out_len = len;
    return killed;
}

// ---- benchmark --------------------------------------------------------------

static int64_t seed = 582;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random() * 32768;
    return high + next_random();
}

int main(void) {
    int64_t count = 20;
    int64_t rounds = 30;
    int64_t n = 50000;
    int64_t *pids[20];
    int64_t *ppids[20];
    int64_t *names = malloc(n * sizeof(int64_t));
    for (int64_t g = 0; g < count; g++) {
        for (int64_t i = 0; i < n; i++) {
            names[i] = i + 1;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = wide() % (i + 1);
            int64_t t = names[i];
            names[i] = names[j];
            names[j] = t;
        }
        pids[g] = malloc(n * sizeof(int64_t));
        ppids[g] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            pids[g][i] = names[i];
            ppids[g][i] = i == 0 ? 0 : names[wide() % i];
        }
    }
    free(names);
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int64_t kill = (round + g) % 4 == 0 ? pids[p][0] : pids[p][wide() % n];
            int64_t len;
            int64_t *got = kill_process(pids[p], ppids[p], n, kill, &len);
            int64_t sum = 0;
            for (int64_t k = 0; k < len; k++) {
                sum += got[k];
            }
            free(got);
            total += len;
            checksum = (checksum * 31 + sum) % 1000000007;
        }
    }
    printf("%lld trees of 50000 processes, %lld rounds: %lld killed, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free(pids[g]);
        free(ppids[g]);
    }
    return 0;
}
