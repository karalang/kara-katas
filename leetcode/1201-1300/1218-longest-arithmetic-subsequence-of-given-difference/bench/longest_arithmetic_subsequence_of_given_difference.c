// LeetCode #1218 bench, in C: the ★ arm (a hash table from each value to
// the longest subsequence ending with it, open addressing with linear
// probing, cleared per call) on 16 arrays of 10^5 values from -10^4 to
// 10^4 drawn once, each asked with the differences -3 to 3; every answer
// folded into a checksum.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000
#define SLOTS 65536

static long long seed = 1218;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long keys[SLOTS], vals[SLOTS];
static char used[SLOTS];

static unsigned slot_of(long long k) {
    unsigned long long h = (unsigned long long)k * 0x9E3779B97F4A7C15ULL;
    return (unsigned)(h >> 48);
}

static long long get(long long k) {
    unsigned s = slot_of(k);
    while (used[s]) {
        if (keys[s] == k) return vals[s];
        s = (s + 1) & (SLOTS - 1);
    }
    return 0;
}

static void put(long long k, long long v) {
    unsigned s = slot_of(k);
    while (used[s] && keys[s] != k) s = (s + 1) & (SLOTS - 1);
    used[s] = 1;
    keys[s] = k;
    vals[s] = v;
}

static long long longest_subsequence(const long long *arr, int n, long long difference) {
    memset(used, 0, sizeof used);
    long long best = 0;
    for (int i = 0; i < n; i++) {
        long long length = get(arr[i] - difference) + 1;
        put(arr[i], length);
        if (length > best) best = length;
    }
    return best;
}

int main(void) {
    long long *arrays = malloc(sizeof(long long) * 16 * N);
    for (int a = 0; a < 16; a++)
        for (int i = 0; i < N; i++) arrays[a * N + i] = next_random() % 20001 - 10000;
    long long check = 0;
    for (int a = 0; a < 16; a++)
        for (long long d = -3; d <= 3; d++)
            check = (check * 131 + longest_subsequence(arrays + a * N, N, d) + d + 3) % 1000000007LL;
    printf("16 arrays of 10^5 values, differences -3 to 3: checksum %lld\n", check);
    free(arrays);
    return 0;
}
