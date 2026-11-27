// LeetCode #1817: Finding the Users Active Minutes -- the bench in C: the
// ★ arm over 5000 calls on runs of 5000 to 9999 logs cut from one list of
// 10^4 logs over 1000 users and 100 minutes, built once, each run's length
// drawn from the checksum so far. The map of sets is one open-addressing
// hash table of (user, minute) pairs, for the distinct pairs, and one of
// users, for their counts.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint64_t mix(uint64_t k) {
    k ^= k >> 33;
    k *= 0xff51afd7ed558ccdULL;
    k ^= k >> 33;
    k *= 0xc4ceb9fe1a85ec53ULL;
    k ^= k >> 33;
    return k;
}

typedef struct {
    int64_t *keys;
    int64_t *vals;
    char *used;
    size_t cap;
} Table;

static Table table(size_t cap) {
    Table t = {malloc(cap * sizeof(int64_t)), calloc(cap, sizeof(int64_t)), calloc(cap, 1), cap};
    return t;
}

static int64_t *slot(Table *t, int64_t key, int *fresh) {
    size_t at = mix((uint64_t)key) & (t->cap - 1);
    while (t->used[at] && t->keys[at] != key)
        at = (at + 1) & (t->cap - 1);
    *fresh = !t->used[at];
    t->used[at] = 1;
    t->keys[at] = key;
    return &t->vals[at];
}

static void drop(Table *t) {
    free(t->keys);
    free(t->vals);
    free(t->used);
}

static int64_t *finding_users_active_minutes(const int64_t (*logs)[2], size_t n, int64_t k) {
    size_t cap = 1;
    while (cap < 2 * n)
        cap <<= 1;
    Table pairs = table(cap), users = table(cap);
    for (size_t i = 0; i < n; i++) {
        int fresh;
        slot(&pairs, logs[i][0] * 1000000 + logs[i][1], &fresh);
        if (fresh)
            (*slot(&users, logs[i][0], &fresh))++;
    }
    int64_t *answer = calloc((size_t)k, sizeof(int64_t));
    for (size_t i = 0; i < users.cap; i++)
        if (users.used[i])
            answer[users.vals[i] - 1]++;
    drop(&pairs);
    drop(&users);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1817;
    static int64_t base[10000][2];
    for (int i = 0; i < 10000; i++) {
        base[i][0] = next_random(&seed) % 1000;
        base[i][1] = next_random(&seed) % 100;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 5000; call++) {
        size_t n = (size_t)(5000 + (check + call) % 5000);
        int64_t *answer = finding_users_active_minutes((const int64_t (*)[2])base, n, 100);
        for (int j = 0; j < 100; j++)
            check = (check * 31 + answer[j]) % 1000000007;
        free(answer);
    }
    printf("5000 calls: checksum %lld\n", (long long)check);
    return 0;
}
