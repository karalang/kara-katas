// LeetCode #954: Array of Doubled Pairs -- C mirror of the Kara bench
// program (counts, smallest first). The counts sit in an open-addressing
// table with linear probing, sized at least twice the values.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long *keys;
    long *counts;
    bool *used;
    long mask;
    int shift;
} Table;

static long slot(const Table *t, long key) {
    long i = (long)(((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> t->shift);
    while (t->used[i] && t->keys[i] != key) {
        i = (i + 1) & t->mask;
    }
    return i;
}

static long get(const Table *t, long key) {
    long i = slot(t, key);
    return t->used[i] ? t->counts[i] : 0;
}

static int by_abs(const void *a, const void *b) {
    long x = labs(*(const long *)a), y = labs(*(const long *)b);
    return (x > y) - (x < y);
}

static bool can_reorder_doubled(const long *arr, long n) {
    long cap = 1;
    int bits = 0;
    while (cap < 2 * n) {
        cap *= 2;
        bits++;
    }
    Table t = {malloc(sizeof(long) * cap), malloc(sizeof(long) * cap), calloc(cap, 1), cap - 1, 64 - bits};
    long *values = malloc(sizeof(long) * n);
    long distinct = 0;
    for (long k = 0; k < n; k++) {
        long i = slot(&t, arr[k]);
        if (!t.used[i]) {
            t.used[i] = true;
            t.keys[i] = arr[k];
            t.counts[i] = 0;
            values[distinct++] = arr[k];
        }
        t.counts[i]++;
    }
    qsort(values, distinct, sizeof(long), by_abs);
    bool ok = true;
    for (long k = 0; k < distinct && ok; k++) {
        long x = values[k];
        long c = get(&t, x);
        if (c == 0) {
            continue;
        }
        if (x == 0) {
            if (c % 2 != 0) {
                ok = false;
            }
            continue;
        }
        long i = slot(&t, 2 * x);
        long d = t.used[i] ? t.counts[i] : 0;
        if (d < c) {
            ok = false;
        } else {
            t.counts[i] = d - c;
        }
    }
    free(t.keys);
    free(t.counts);
    free(t.used);
    free(values);
    return ok;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    const long rounds = 10, count = 20, n = 30000;
    long seed = 954;
    long **sets = malloc(sizeof(long *) * count);
    for (long s = 0; s < count; s++) {
        long *arr = malloc(sizeof(long) * n);
        for (long i = 0; i < n / 2; i++) {
            long a = next_random(&seed);
            long x = (a * 32768 + next_random(&seed)) % 100001 - 50000;
            arr[2 * i] = x;
            arr[2 * i + 1] = 2 * x;
        }
        for (long i = 0; i < n; i++) {
            long a = next_random(&seed);
            long j = i + (a * 32768 + next_random(&seed)) % (n - i);
            long t = arr[i];
            arr[i] = arr[j];
            arr[j] = t;
        }
        if (s % 4 == 3) {
            arr[s * 1000] = 2 * (arr[s * 1000] / 2) + 1;
        }
        sets[s] = arr;
    }
    long yes = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (long i = 0; i < count; i++) {
            long k = (r + i) % count;
            bool ok = can_reorder_doubled(sets[k], n);
            if (ok) {
                yes++;
            }
            check = (check * 31 + (ok ? 1 : 2)) % 1000000007;
        }
    }
    printf("%ld rounds over %ld sets of %ld values: %ld can be paired, checksum %ld\n", rounds, count, n, yes, check);
    return 0;
}
