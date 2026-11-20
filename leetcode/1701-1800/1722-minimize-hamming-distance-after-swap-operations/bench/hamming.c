// LeetCode #1722: Minimize Hamming Distance After Swap Operations -- the
// bench (hamming.kara): the swaps joined into groups with a union-find,
// each group's source values counted, and each target value matched from
// its group's counts.
//
// C has no map: a table of 2^18 slots probed linearly, the key (group,
// value) packed into one 64-bit word and hashed by one multiply.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 18)

static uint64_t keys[SLOTS];
static long counts[SLOTS];
static char used[SLOTS];

static long *slot(uint64_t key) {
    uint64_t h = (key * 0x9E3779B97F4A7C15ULL) >> 46;
    while (used[h] && keys[h] != key) {
        h = (h + 1) & (SLOTS - 1);
    }
    if (!used[h]) {
        used[h] = 1;
        keys[h] = key;
        counts[h] = 0;
    }
    return &counts[h];
}

static long *lookup(uint64_t key) {
    uint64_t h = (key * 0x9E3779B97F4A7C15ULL) >> 46;
    while (used[h]) {
        if (keys[h] == key) {
            return &counts[h];
        }
        h = (h + 1) & (SLOTS - 1);
    }
    return NULL;
}

static long find(long *parent, long x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int minimum_hamming_distance(const int *source, const int *target, long n, const int (*allowed)[2], long m) {
    long *parent = malloc(sizeof(long) * n);
    long *size = malloc(sizeof(long) * n);
    for (long i = 0; i < n; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    for (long s = 0; s < m; s++) {
        long a = find(parent, allowed[s][0]);
        long b = find(parent, allowed[s][1]);
        if (a == b) {
            continue;
        }
        if (size[a] < size[b]) {
            long t = a;
            a = b;
            b = t;
        }
        parent[b] = a;
        size[a] += size[b];
    }
    memset(used, 0, sizeof used);
    for (long i = 0; i < n; i++) {
        *slot(((uint64_t)find(parent, i) << 32) | (uint32_t)source[i]) += 1;
    }
    int distance = 0;
    for (long i = 0; i < n; i++) {
        long *c = lookup(((uint64_t)find(parent, i) << 32) | (uint32_t)target[i]);
        if (c != NULL && *c > 0) {
            *c -= 1;
        } else {
            distance++;
        }
    }
    free(parent);
    free(size);
    return distance;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static long wide(long *seed) {
    long hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    int count = 10;
    long rounds = 5;
    long n = 100000;
    long seed = 1722;
    int *sources[10], *targets[10];
    int (*alloweds[10])[2];
    for (int c = 0; c < count; c++) {
        sources[c] = malloc(sizeof(int) * n);
        targets[c] = malloc(sizeof(int) * n);
        alloweds[c] = malloc(sizeof(int[2]) * n);
        for (long i = 0; i < n; i++) {
            sources[c][i] = (int)(wide(&seed) % 100000 + 1);
        }
        for (long i = 0; i < n; i++) {
            targets[c][i] = (int)(wide(&seed) % 100000 + 1);
        }
        for (long i = 0; i < n; i++) {
            long a = wide(&seed) % n;
            long b = wide(&seed) % (n - 1);
            if (b >= a) {
                b++;
            }
            alloweds[c][i][0] = (int)a;
            alloweds[c][i][1] = (int)b;
        }
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            long answer = minimum_hamming_distance(sources[c], targets[c], n, (const int (*)[2])alloweds[c], n);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %ld values and %ld swaps, %ld rounds: distances sum to %ld, checksum %ld\n", count, n, n, rounds, sum, check);
    for (int c = 0; c < count; c++) {
        free(sources[c]);
        free(targets[c]);
        free(alloweds[c]);
    }
    return 0;
}
