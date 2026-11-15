// LeetCode #2189: Number of Ways to Build House of Cards -- the
// benchmark's C mirror of cards.kara: a 0/1 knapsack over the row
// widths, into a buffer malloc'd per solve as the Kāra arm's list is.

#include <stdio.h>
#include <stdlib.h>

static long long house_of_cards(long long n) {
    long long *ways = calloc(n + 1, sizeof(long long));
    ways[0] = 1;
    for (long long k = 1; 3 * k - 1 <= n; k++) {
        long long cost = 3 * k - 1;
        for (long long s = n; s >= cost; s--) ways[s] += ways[s - cost];
    }
    long long r = ways[n];
    free(ways);
    return r;
}

static long long seed = 2189;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long check = 0;
    for (int i = 0; i < 20000; i++) {
        long long n = next_random() % 500 + 1;
        check = (check * 31 + house_of_cards(n) % 1000000007) % 1000000007;
    }
    printf("20000 solves: checksum %lld\n", check);
    return 0;
}
