// LeetCode #1055: Shortest Way to Form String -- C mirror of
// bench/shortest_way.kara.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 1055;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long shortest_way(const char *s, long long n, const char *t, long long m) {
    long long pieces = 0, i = 0;
    while (i < m) {
        long long start = i;
        for (long long k = 0; k < n; k++)
            if (i < m && t[i] == s[k]) i++;
        if (i == start) return -1;
        pieces++;
    }
    return pieces;
}

static char *random_word(long long n) {
    char *w = malloc(n);
    for (long long k = 0; k < n; k++) w[k] = (char)(97 + next_random() % 20);
    return w;
}

int main(void) {
    enum { COUNT = 100, ROUNDS = 10, N = 1000, M = 10000 };
    char *sources[COUNT], *targets[COUNT];
    for (int a = 0; a < COUNT; a++) {
        sources[a] = random_word(N);
        targets[a] = random_word(M);
    }
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int a = 0; a < COUNT; a++) {
            long long answer = shortest_way(sources[a], N, targets[a], M);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    printf("%d pairs of 1000 and 10000 letters, %d rounds: total %lld, checksum %lld\n", COUNT, ROUNDS, total, check);
    for (int a = 0; a < COUNT; a++) {
        free(sources[a]);
        free(targets[a]);
    }
    return 0;
}
