// LeetCode #2078: Two Furthest Houses With Different Colors -- C mirror of
// the ★ arm's benchmark (houses.kara): 20000 streets of 100 houses, 1000
// rounds each recoloring one house of every street and answering every
// street that still has two colors with a scan in from each end.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 2078;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long max_distance(const long long *colors, long long n) {
    long long j = n - 1;
    while (colors[j] == colors[0]) j--;
    long long i = 0;
    while (colors[i] == colors[n - 1]) i++;
    return j > n - 1 - i ? j : n - 1 - i;
}

int main(void) {
    long long *streets = calloc(20000 * 100, sizeof(long long));
    for (int s = 0; s < 20000; s++) {
        long long *colors = streets + 100 * s;
        long long a = next_random() % 100;
        colors[a] = next_random() % 3 + 1;
        long long b = next_random() % 100;
        colors[b] = next_random() % 3 + 1;
    }
    long long answered = 0, total = 0, check = 0;
    for (int r = 0; r < 1000; r++) {
        for (int s = 0; s < 20000; s++) {
            long long *colors = streets + 100 * s;
            long long k = next_random() % 100;
            colors[k] = next_random() % 2 == 0 ? 0 : next_random() % 3 + 1;
            int mixed = 0;
            for (int h = 0; h < 100; h++)
                if (colors[h] != colors[0]) {
                    mixed = 1;
                    break;
                }
            if (mixed) {
                long long d = max_distance(colors, 100);
                answered++;
                total += d;
                check = (check * 31 + d) % 1000000007;
            }
        }
    }
    printf("%lld answers: sum %lld, checksum %lld\n", answered, total, check);
    free(streets);
    return 0;
}
