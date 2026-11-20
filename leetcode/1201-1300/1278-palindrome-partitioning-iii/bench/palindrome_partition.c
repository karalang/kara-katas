// LeetCode #1278 bench, in C: the ★ arm (the changes for every substring,
// then the fewest for each prefix in each number of pieces) on 200 random
// strings of 100 letters from 2 to 26, each cut into 1 to 100 pieces,
// drawn once; 20 rounds, every answer folded into a checksum. The tables
// are allocated per call, as the other languages' are.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long palindrome_partition(const char *s, int k) {
    int n = (int)strlen(s);
    long long *cost = calloc((size_t)n * n, sizeof(long long));
    for (int len = 2; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            long long inner = len > 2 ? cost[(i + 1) * n + j - 1] : 0;
            cost[i * n + j] = inner + (s[i] != s[j] ? 1 : 0);
        }
    long long unreachable = n + 1;
    long long *best = malloc(sizeof(long long) * (k + 1) * (n + 1));
    for (int x = 0; x < (k + 1) * (n + 1); x++) best[x] = unreachable;
    best[0] = 0;
    for (int p = 1; p <= k; p++)
        for (int j = p; j <= n; j++)
            for (int i = p - 1; i < j; i++) {
                long long through = best[(p - 1) * (n + 1) + i] + cost[i * n + j - 1];
                if (through < best[p * (n + 1) + j]) best[p * (n + 1) + j] = through;
            }
    long long answer = best[k * (n + 1) + n];
    free(cost);
    free(best);
    return answer;
}

static long long seed = 1278;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    static char strings[200][101];
    int ks[200];
    for (int c = 0; c < 200; c++) {
        long long letters = next_random() % 25 + 2;
        for (int x = 0; x < 100; x++) strings[c][x] = alphabet[next_random() % letters];
        strings[c][100] = 0;
        ks[c] = (int)(next_random() % 100 + 1);
    }
    long long check = 0;
    for (long long round = 0; round < 20; round++)
        for (int c = 0; c < 200; c++)
            check = (check * 131 + palindrome_partition(strings[c], ks[c]) + round) % 1000000007;
    printf("20 rounds of 200 strings of 100 letters: checksum %lld\n", check);
    return 0;
}
