// LeetCode #2365: Task Scheduler II -- the bench, the ★ arm in C: the day
// goes forward one for each task, and jumps to the day after the type's
// last run plus `space` when that is later; a hash map keeps each type's
// last day. C has no hash map, so this one is open addressing with linear
// probing over a table of 2^18 slots, the key mixed by splitmix64's
// finalizer.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 18)

static uint64_t mix(uint64_t x) {
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return x;
}

static int64_t task_scheduler_ii(const int64_t *tasks, int64_t n, int64_t space) {
    int64_t *keys = malloc(SLOTS * sizeof(int64_t));
    int64_t *last = malloc(SLOTS * sizeof(int64_t));
    memset(last, 0, SLOTS * sizeof(int64_t));
    int64_t day = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t task = tasks[i];
        day++;
        uint64_t s = mix((uint64_t)task) & (SLOTS - 1);
        while (last[s] != 0 && keys[s] != task) {
            s = (s + 1) & (SLOTS - 1);
        }
        if (last[s] != 0 && last[s] + space + 1 > day) {
            day = last[s] + space + 1;
        }
        keys[s] = task;
        last[s] = day;
    }
    free(keys);
    free(last);
    return day;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    // list a: 10^5 tasks of 4^(a / 2 + 1) types (at most 10^5) up to
    // 10^9, with a space of 3^a
    const int64_t n = 100000;
    int64_t seed = 2365;
    int64_t *lists[10];
    int64_t spaces[10];
    int64_t *types = malloc(100000 * sizeof(int64_t));
    int64_t space = 1;
    for (int64_t a = 0; a < 10; a++) {
        int64_t kinds = (int64_t)1 << (2 * (a / 2 + 1));
        if (kinds > 100000) {
            kinds = 100000;
        }
        for (int64_t k = 0; k < kinds; k++) {
            types[k] = 1 + wide_random(&seed) % 1000000000;
        }
        lists[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            lists[a][i] = types[wide_random(&seed) % kinds];
        }
        spaces[a] = space;
        space *= 3;
    }
    free(types);
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int a = 0; a < 10; a++) {
            check = (check * 31 + task_scheduler_ii(lists[a], n, spaces[a]) % 1000000007 + p) % 1000000007;
        }
    }
    printf("20 passes over 10 lists of 10^5 tasks: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(lists[a]);
    }
    return 0;
}
