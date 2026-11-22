// LeetCode #2766: Relocate Marbles -- the bench (marbles.kara in C): the
// occupied positions in a hash set, open addressing with linear probing
// and tombstones, each move taking its from position out and putting its
// to position in; the set gathered and sorted by `qsort` at the end.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define EMPTY 0
#define GONE (-1)
#define BITS 19
#define CAP (1 << BITS)

static int64_t seed = 2766;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static uint64_t hash(int64_t x) {
    uint64_t z = (uint64_t)x + 0x9e3779b97f4a7c15ULL;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return (z ^ (z >> 31)) >> (64 - BITS);
}

// positions are at least 1, so 0 marks an empty slot and -1 a removed one
static void set_insert(int64_t *table, int64_t x) {
    uint64_t i = hash(x);
    int64_t tomb = -1;
    while (table[i] != EMPTY) {
        if (table[i] == x) return;
        if (table[i] == GONE && tomb < 0) tomb = (int64_t)i;
        i = (i + 1) & (CAP - 1);
    }
    table[tomb >= 0 ? (uint64_t)tomb : i] = x;
}

static void set_remove(int64_t *table, int64_t x) {
    uint64_t i = hash(x);
    while (table[i] != EMPTY) {
        if (table[i] == x) { table[i] = GONE; return; }
        i = (i + 1) & (CAP - 1);
    }
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t relocate_marbles(const int64_t *nums, int64_t n, const int64_t *move_from, const int64_t *move_to, int64_t m, int64_t *table, int64_t *out) {
    memset(table, 0, sizeof(int64_t) * CAP);
    for (int64_t i = 0; i < n; i++) set_insert(table, nums[i]);
    for (int64_t i = 0; i < m; i++) {
        set_remove(table, move_from[i]);
        set_insert(table, move_to[i]);
    }
    int64_t k = 0;
    for (int64_t i = 0; i < CAP; i++)
        if (table[i] > 0) out[k++] = table[i];
    qsort(out, k, sizeof(int64_t), cmp);
    return k;
}

static void make_case(int64_t n, int64_t moves, int64_t top, int64_t *nums, int64_t *move_from, int64_t *move_to) {
    int64_t *places = malloc(sizeof(int64_t) * (n + moves));
    int64_t *slot = malloc(sizeof(int64_t) * (top + 1));
    int64_t len = 0;
    for (int64_t i = 0; i <= top; i++) slot[i] = -1;
    for (int64_t i = 0; i < n; i++) nums[i] = wide() % top + 1;
    for (int64_t i = 0; i < n; i++)
        if (slot[nums[i]] < 0) { slot[nums[i]] = len; places[len++] = nums[i]; }
    for (int64_t i = 0; i < moves; i++) {
        int64_t a = places[wide() % len];
        int64_t b = wide() % top + 1;
        move_from[i] = a;
        move_to[i] = b;
        if (a != b) {
            int64_t k = slot[a];
            slot[a] = -1;
            int64_t last = places[--len];
            if (last != a) { places[k] = last; slot[last] = k; }
            if (slot[b] < 0) { slot[b] = len; places[len++] = b; }
        }
    }
    free(places); free(slot);
}

int main(void) {
    const int count = 20, rounds = 5;
    const int64_t n = 100000, top = 1000000;
    int64_t *nums = malloc(sizeof(int64_t) * n * count);
    int64_t *move_from = malloc(sizeof(int64_t) * n * count);
    int64_t *move_to = malloc(sizeof(int64_t) * n * count);
    int64_t *table = malloc(sizeof(int64_t) * CAP);
    int64_t *out = malloc(sizeof(int64_t) * CAP);
    for (int c = 0; c < count; c++) make_case(n, n, top, nums + n * c, move_from + n * c, move_to + n * c);
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int c = 0; c < count; c++) {
            int64_t k = relocate_marbles(nums + n * c, n, move_from + n * c, move_to + n * c, n, table, out);
            sum += k;
            check = (check * 31 + k + r) % 1000000007;
            for (int64_t i = 0; i < k; i++) check = (check * 31 + out[i]) % 1000000007;
        }
    printf("%d cases of 100000 marbles and moves, %d rounds: %lld places, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(nums); free(move_from); free(move_to); free(table); free(out);
    return 0;
}
