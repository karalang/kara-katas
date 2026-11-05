// LeetCode #1054: Distant Barcodes -- C mirror of bench/barcodes.kara.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 1054;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// The answer is written to `answer`, a fresh array of `n`.
static void rearrange_barcodes(const long long *barcodes, long long n, long long *answer) {
    long long top = barcodes[0];
    for (long long k = 1; k < n; k++)
        if (barcodes[k] > top) top = barcodes[k];
    long long *counts = calloc(top + 1, sizeof(long long));
    for (long long k = 0; k < n; k++) counts[barcodes[k]]++;
    long long most = 0;
    for (long long v = 1; v < top + 1; v++)
        if (counts[v] > counts[most]) most = v;
    long long place = 0, v = most, next = 1;
    for (long long k = 0; k < n; k++) {
        while (counts[v] == 0) v = next++;
        answer[place] = v;
        counts[v]--;
        place += 2;
        if (place >= n) place = 1;
    }
    free(counts);
}

int main(void) {
    enum { COUNT = 200, N = 20000, ROUNDS = 25 };
    long long *all = malloc(sizeof(long long) * COUNT * N);
    for (int a = 0; a < COUNT; a++) {
        long long *barcodes = all + (long long)a * N;
        long long common = next_random() % 10000 + 1;
        long long copies = next_random() % 9000 + 1;
        long long k = 0;
        for (; k < copies; k++) barcodes[k] = common;
        for (; k < N; k++) barcodes[k] = next_random() % 10000 + 1;
    }
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int a = 0; a < COUNT; a++) {
            long long *answer = calloc(N, sizeof(long long));
            rearrange_barcodes(all + (long long)a * N, N, answer);
            long long h = 0;
            for (long long k = 0; k < N; k += 97) h = (h * 10007 + answer[k]) % 1000000007;
            total += answer[1];
            check = (check * 131 + h) % 1000000007;
            free(answer);
        }
    }
    printf("%d arrays of %d barcodes, %d rounds: total %lld, checksum %lld\n", COUNT, N, ROUNDS, total, check);
    free(all);
    return 0;
}
