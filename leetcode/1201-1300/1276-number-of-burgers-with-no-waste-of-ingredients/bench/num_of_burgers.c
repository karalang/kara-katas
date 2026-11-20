// LeetCode #1276 bench, in C: the ★ arm (by algebra) on 100,000 random
// pairs of tomato and cheese slice counts up to 10^7, a third made from
// burgers and a third near such a count, drawn once; 1000 rounds, every
// answer folded into a checksum. The answer is LeetCode's C shape, a
// malloc'd array and its size, freed by the caller.
#include <stdio.h>
#include <stdlib.h>

static long long *num_of_burgers(long long t, long long c, int *size) {
    *size = 0;
    if (t % 2 != 0) return NULL;
    long long jumbo = t / 2 - c;
    long long small = 2 * c - t / 2;
    if (jumbo < 0 || small < 0) return NULL;
    long long *answer = malloc(2 * sizeof(long long));
    answer[0] = jumbo;
    answer[1] = small;
    *size = 2;
    return answer;
}

static long long seed = 1276;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static long long ts[100000], cs[100000];
    for (int k = 0; k < 100000; k++) {
        long long jumbo = next_random() % 2500000;
        long long small = next_random() % 2500000;
        long long t, c;
        if (k % 3 == 0) {
            t = 4 * jumbo + 2 * small;
            c = jumbo + small;
        } else if (k % 3 == 1) {
            t = 4 * jumbo + 2 * small + next_random() % 5 - 2;
            c = jumbo + small + next_random() % 3 - 1;
        } else {
            t = next_random() % 10000001;
            c = next_random() % 5000001;
        }
        ts[k] = t < 0 ? 0 : t;
        cs[k] = c < 0 ? 0 : c;
    }
    long long check = 0;
    for (long long round = 0; round < 1000; round++) {
        for (int k = 0; k < 100000; k++) {
            int size;
            long long *answer = num_of_burgers(ts[k] + round, cs[k], &size);
            if (size == 2)
                check = (check * 131 + answer[0] * 7 + answer[1]) % 1000000007;
            else
                check = (check * 131 + 1) % 1000000007;
            free(answer);
        }
    }
    printf("1000 rounds of 100000 pairs: checksum %lld\n", check);
    return 0;
}
