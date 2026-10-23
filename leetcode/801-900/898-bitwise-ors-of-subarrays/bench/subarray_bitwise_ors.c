// LeetCode #898 bench: the table arm (the ★ arm with a hash table of its
// own) on 12 arrays of 50,000 numbers, LeetCode's largest, each a random
// number below 2^30 AND-ed with a second, so that about a quarter of the
// bits are set. The ORs ending at each place are kept in a short list,
// and every one is gathered into an open-addressing hash table written
// here, with no library set, map or sort. The same algorithm as
// subarray_bitwise_ors.kara.
// The short lists are two fixed arrays of 32, swapped at each place.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *slots;
    int64_t len, count;
} Table;

static void insert(Table *t, int64_t v) {
    int64_t mask = t->len - 1;
    int64_t i = ((v * 2654435761) % 4294967296) & mask;
    while (t->slots[i] != -1) {
        if (t->slots[i] == v) return;
        i = (i + 1) & mask;
    }
    t->slots[i] = v;
    t->count++;
    if (t->count * 2 > t->len) {
        int64_t *old = t->slots;
        int64_t old_len = t->len;
        t->len = old_len * 2;
        t->slots = malloc(t->len * sizeof(int64_t));
        for (int64_t k = 0; k < t->len; k++) t->slots[k] = -1;
        t->count = 0;
        for (int64_t k = 0; k < old_len; k++)
            if (old[k] != -1) insert(t, old[k]);
        free(old);
    }
}

static int64_t subarray_bitwise_ors(const int64_t *arr, int64_t n) {
    Table t = {malloc(64 * sizeof(int64_t)), 64, 0};
    for (int k = 0; k < 64; k++) t.slots[k] = -1;
    int64_t a[32], b[32];
    int64_t *ending = a, *next = b;
    int64_t ending_len = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = arr[i];
        int64_t next_len = 0;
        next[next_len++] = x;
        for (int64_t k = 0; k < ending_len; k++) {
            int64_t v = ending[k] | x;
            if (v != next[next_len - 1]) next[next_len++] = v;
        }
        for (int64_t k = 0; k < next_len; k++) insert(&t, next[k]);
        int64_t *swap = ending;
        ending = next;
        next = swap;
        ending_len = next_len;
    }
    free(t.slots);
    return t.count;
}

static int64_t seed = 898;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *arr = malloc(50000 * sizeof(int64_t));
    int64_t total = 0, check = 0;
    for (int r = 0; r < 12; r++) {
        for (int i = 0; i < 50000; i++) {
            int64_t a = next_random() * 32768;
            a += next_random();
            int64_t b = next_random() * 32768;
            b += next_random();
            arr[i] = a & b;
        }
        int64_t got = subarray_bitwise_ors(arr, 50000);
        total += got;
        check = (check * 131 + got) % 1000000007;
    }
    printf("12 arrays of 50000 numbers: %lld ORs in all, checksum %lld\n", (long long)total, (long long)check);
    free(arr);
    return 0;
}
