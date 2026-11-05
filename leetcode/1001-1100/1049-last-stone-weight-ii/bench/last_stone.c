// LeetCode #1049: Last Stone Weight II -- C mirror of bench/last_stone.kara.
// The table of sums is allocated afresh for each list, as the other
// languages' vectors are.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 1049;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long last_stone_weight_ii(const long long *stones, int n) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += stones[i];
    long long half = total / 2;
    char *made = calloc(half + 1, 1);
    made[0] = 1;
    for (int i = 0; i < n; i++) {
        long long s = stones[i];
        for (long long t = half; t >= s; t--)
            if (made[t - s]) made[t] = 1;
    }
    long long best = half;
    while (!made[best]) best--;
    free(made);
    return total - 2 * best;
}

int main(void) {
    enum { LISTS = 1000, COUNT = 30, ROUNDS = 10 };
    static long long all[LISTS][COUNT];
    for (int l = 0; l < LISTS; l++)
        for (int i = 0; i < COUNT; i++) all[l][i] = next_random() % 100 + 1;
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int l = 0; l < LISTS; l++) {
            long long answer = last_stone_weight_ii(all[l], COUNT);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    printf("%d lists of %d stones, %d rounds: total %lld, checksum %lld\n", LISTS, COUNT, ROUNDS, total, check);
    return 0;
}
