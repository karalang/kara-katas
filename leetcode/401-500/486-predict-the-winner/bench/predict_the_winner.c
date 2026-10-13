// Benchmark for #486: C mirror of the ★ arm (one row of leads); see
// predict_the_winner.kara.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int predict_the_winner(const long long *nums, long long n) {
    long long *d = malloc(sizeof(long long) * n);
    memcpy(d, nums, sizeof(long long) * n);
    for (long long i = n - 2; i >= 0; i--) {
        for (long long j = i + 1; j < n; j++) {
            long long left = nums[i] - d[j], right = nums[j] - d[j - 1];
            d[j] = left > right ? left : right;
        }
    }
    int win = d[n - 1] >= 0;
    free(d);
    return win;
}

int main(void) {
    long long *arrays[200], sizes[200];
    long long seed = 486;
    for (int a = 0; a < 200; a++) {
        sizes[a] = 1000 + a % 2;
        arrays[a] = malloc(sizeof(long long) * sizes[a]);
        for (long long i = 0; i < sizes[a]; i++) {
            arrays[a][i] = next_random(&seed) * 32768 % 10000001;
        }
    }
    long long wins = 0, checksum = 0;
    for (int a = 0; a < 200; a++) {
        long long win = predict_the_winner(arrays[a], sizes[a]);
        wins += win;
        checksum = (checksum * 31 + win * 7 + sizes[a]) % 1000000007;
    }
    printf("200 arrays of 1000 or 1001 numbers: player 1 wins %lld, checksum %lld\n", wins, checksum);
    return 0;
}
