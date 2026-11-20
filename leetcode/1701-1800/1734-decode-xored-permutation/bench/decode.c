// LeetCode #1734: Decode XORed Permutation -- the bench (decode.kara): the
// first value from the XOR of 1 to n less that of the codes at odd places,
// then each next value the last XORed with its code.

#include <stdio.h>
#include <stdlib.h>

/* the permutation, n values, in a fresh allocation */
static int *decode(const int *encoded, long n) {
    int all = 0;
    for (long v = 1; v <= n; v++) all ^= (int)v;
    int rest = 0;
    for (long i = 1; i < n - 1; i += 2) rest ^= encoded[i];
    int *perm = malloc(sizeof(int) * n);
    long len = 0;
    perm[len++] = all ^ rest;
    for (long i = 0; i < n - 1; i++) {
        perm[len] = perm[len - 1] ^ encoded[i];
        len++;
    }
    return perm;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static long wide(long *seed) {
    long hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    int count = 50;
    long rounds = 40;
    long n = 99999;
    long seed = 1734;
    int **problems = malloc(sizeof(int *) * count);
    int *perm = malloc(sizeof(int) * n);
    for (int p = 0; p < count; p++) {
        for (long v = 0; v < n; v++) perm[v] = (int)(v + 1);
        for (long i = n - 1; i >= 1; i--) {
            long j = wide(&seed) % (i + 1);
            int t = perm[i];
            perm[i] = perm[j];
            perm[j] = t;
        }
        problems[p] = malloc(sizeof(int) * (n - 1));
        for (long i = 0; i < n - 1; i++) problems[p][i] = perm[i] ^ perm[i + 1];
    }
    free(perm);
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            int *got = decode(problems[p], n);
            sum += got[0];
            check = (check * 31 + got[0] + got[n / 2] + got[n - 1] + r) % 1000000007;
            free(got);
        }
    }
    for (int p = 0; p < count; p++) free(problems[p]);
    free(problems);
    printf("%d permutations of %ld, %ld rounds: first values sum to %ld, checksum %ld\n", count, n, rounds, sum, check);
    return 0;
}
