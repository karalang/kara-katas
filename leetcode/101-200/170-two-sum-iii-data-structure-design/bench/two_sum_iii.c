#include <stdio.h>
#include <stdlib.h>

// Hand-rolled equivalent of the Map: a direct-address count table over [0, K)
// plus a distinct-key list (appended when a key first goes 0 -> positive).
#define K 6000

static long count[K];
static long keys[K];
static long nkeys = 0;

static void add(long number) {
    if (count[number] == 0) {
        keys[nkeys++] = number;
    }
    count[number]++;
}

static int find(long value) {
    int found = 0;
    for (long ki = 0; ki < nkeys; ki++) {
        long k = keys[ki];
        long complement = value - k;
        if (complement == k) {
            if (count[k] >= 2) found = 1;
        } else {
            if (complement >= 0 && complement < K && count[complement] > 0) found = 1;
        }
    }
    return found;
}

int main(void) {
    long k_range = K;
    long n_add = 170, m_query = 1200000;

    long state = 12345;
    for (long i = 0; i < n_add; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        add(state % k_range);
    }

    long sink = 0;
    for (long q = 0; q < m_query; q++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long target = state % (2 * k_range);
        if (find(target)) sink++;
    }
    printf("%ld\n", sink);
    return 0;
}
