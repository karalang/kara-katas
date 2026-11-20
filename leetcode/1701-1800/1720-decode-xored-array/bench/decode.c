// LeetCode #1720: Decode XORed Array -- the bench (decode.kara): each
// value the one before it XORed with the code between them.

#include <stdio.h>
#include <stdlib.h>

/* the decoded array, n + 1 values, in a fresh allocation */
static int *decode(const int *encoded, long n, int first) {
    int *arr = malloc(sizeof(int) * (n + 1));
    long len = 0;
    arr[len++] = first;
    for (long i = 0; i < n; i++) {
        arr[len] = arr[len - 1] ^ encoded[i];
        len++;
    }
    return arr;
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
    int count = 200;
    long rounds = 100;
    long n = 10000;
    long seed = 1720;
    int *encoded[200];
    int firsts[200];
    for (int c = 0; c < count; c++) {
        encoded[c] = malloc(sizeof(int) * n);
        for (long i = 0; i < n; i++) {
            encoded[c][i] = (int)(wide(&seed) % 100001);
        }
        firsts[c] = (int)(wide(&seed) % 100001);
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            int *arr = decode(encoded[c], n, firsts[c]);
            sum += arr[n];
            check = (check * 31 + arr[n / 2] + arr[n] + r) % 1000000007;
            free(arr);
        }
    }
    printf("%d arrays of %ld codes, %ld rounds: last values sum to %ld, checksum %ld\n", count, n, rounds, sum, check);
    for (int c = 0; c < count; c++) {
        free(encoded[c]);
    }
    return 0;
}
