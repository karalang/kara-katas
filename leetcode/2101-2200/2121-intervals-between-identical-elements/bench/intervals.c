// LeetCode #2121: Intervals Between Identical Elements -- the benchmark,
// the same algorithm as intervals.kara: each value's indices gathered in
// a hash map (open addressing, linear probing) of growable lists, then
// one running sum per list.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t *data; int64_t len, cap; } List;
typedef struct { int64_t key; int64_t list; int used; } Slot;

static uint64_t hash(int64_t k) {
    uint64_t x = (uint64_t)k * 0x9E3779B97F4A7C15ULL;
    x ^= x >> 31;
    x *= 0xBF58476D1CE4E5B9ULL;
    return x ^ (x >> 29);
}

static int64_t *get_distances(const int64_t *arr, int64_t n) {
    size_t cap = 16;
    while (cap < (size_t)n * 2) cap <<= 1;
    Slot *t = calloc(cap, sizeof(Slot));
    List *lists = malloc(sizeof(List) * (size_t)n);
    int64_t groups = 0;
    for (int64_t i = 0; i < n; i++) {
        size_t j = hash(arr[i]) & (cap - 1);
        while (t[j].used && t[j].key != arr[i]) j = (j + 1) & (cap - 1);
        if (!t[j].used) {
            t[j].used = 1;
            t[j].key = arr[i];
            t[j].list = groups;
            lists[groups].data = NULL;
            lists[groups].len = lists[groups].cap = 0;
            groups++;
        }
        List *l = &lists[t[j].list];
        if (l->len == l->cap) {
            l->cap = l->cap ? l->cap * 2 : 4;
            l->data = realloc(l->data, sizeof(int64_t) * (size_t)l->cap);
        }
        l->data[l->len++] = i;
    }
    int64_t *answer = calloc((size_t)n, sizeof(int64_t));
    for (int64_t g = 0; g < groups; g++) {
        const int64_t *p = lists[g].data;
        int64_t c = lists[g].len, total = 0, before = 0;
        for (int64_t k = 0; k < c; k++) total += p[k];
        for (int64_t k = 0; k < c; k++) {
            int64_t after = total - before - p[k];
            answer[p[k]] = k * p[k] - before + after - (c - k - 1) * p[k];
            before += p[k];
        }
        free(lists[g].data);
    }
    free(lists);
    free(t);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2121;
    static int64_t arrays[40][50000];
    const int64_t tops[4] = {10, 100, 1000, 10000};
    for (int g = 0; g < 40; g++)
        for (int i = 0; i < 50000; i++) arrays[g][i] = next_random(&seed) % tops[g % 4] + 1;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int64_t g = 0; g < 40; g++) {
            arrays[g][(round * 7919 + g * 104729) % 50000] += 1;
            int64_t *answer = get_distances(arrays[g], 50000);
            int64_t sum = 0;
            for (int i = 0; i < 50000; i++) sum += answer[i];
            free(answer);
            total += sum;
            check = (check * 31 + sum % 1000000007) % 1000000007;
        }
    }
    printf("800 solves: distances sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
