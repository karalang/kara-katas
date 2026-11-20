// LeetCode #1207 bench, in C: the ★ arm (each value's count in a hash map,
// and the counts put in a hash set) on 2000 arrays of 1000 values drawn
// once, then 10 rounds over the arrays, how many answer true folded into a
// checksum. The map and the set are open-addressed tables with linear
// probing, 2048 slots, cleared for each array.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 2048

static long long seed = 1207;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static unsigned slot_of(long long key) {
    return (unsigned)(((unsigned long long)key * 11400714819323198485ULL) >> 53);
}

static int unique_occurrences(const long long *arr, int n) {
    static long long keys[SLOTS], counts[SLOTS], set[SLOTS];
    static char used[SLOTS], in_set[SLOTS];
    memset(used, 0, sizeof used);
    memset(in_set, 0, sizeof in_set);
    int distinct_values = 0;
    for (int i = 0; i < n; i++) {
        unsigned s = slot_of(arr[i]);
        while (used[s] && keys[s] != arr[i]) s = (s + 1) & (SLOTS - 1);
        if (!used[s]) {
            used[s] = 1;
            keys[s] = arr[i];
            counts[s] = 0;
            distinct_values++;
        }
        counts[s]++;
    }
    int distinct_counts = 0;
    for (int s = 0; s < SLOTS; s++) {
        if (!used[s]) continue;
        unsigned t = slot_of(counts[s]);
        while (in_set[t] && set[t] != counts[s]) t = (t + 1) & (SLOTS - 1);
        if (!in_set[t]) {
            in_set[t] = 1;
            set[t] = counts[s];
            distinct_counts++;
        }
    }
    return distinct_counts == distinct_values;
}

int main(void) {
    static long long arrays[2000][1000];
    for (int a = 0; a < 2000; a++) {
        long long k = next_random() % 12 + 1;
        long long values[12];
        for (int j = 0; j < k; j++) values[j] = next_random() % 2001 - 1000;
        long long total = k * (k + 1) / 2;
        for (int i = 0; i < 1000; i++) {
            long long r = next_random() % total;
            long long j = 0;
            while (r > j) {
                r -= j + 1;
                j++;
            }
            arrays[a][i] = values[j];
        }
    }
    long long check = 0;
    for (int round = 0; round < 10; round++) {
        long long yes = 0;
        for (int a = 0; a < 2000; a++) yes += unique_occurrences(arrays[a], 1000);
        check = (check * 131 + yes + round) % 1000000007;
    }
    printf("10 rounds over 2000 arrays of 1000 values: checksum %lld\n", check);
    return 0;
}
