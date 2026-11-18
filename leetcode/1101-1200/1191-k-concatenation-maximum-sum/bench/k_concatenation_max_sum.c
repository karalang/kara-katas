// LeetCode #1191 bench: the ★ arm in C, over the same 4 arrays of 10^5
// values and 200 rounds as the Kāra bench.

#include <stdio.h>
#include <stdlib.h>

#define N 100000

static long k_concatenation_max_sum(const long *arr, long n, long k) {
    long total = 0;
    for (long i = 0; i < n; i++) {
        total += arr[i];
    }
    long best = 0, run = 0;
    long copies = k < 2 ? k : 2;
    for (long c = 0; c < copies; c++) {
        for (long i = 0; i < n; i++) {
            run += arr[i];
            if (run < 0) {
                run = 0;
            }
            if (run > best) {
                best = run;
            }
        }
    }
    if (k > 2 && total > 0) {
        best += (k - 2) * total;
    }
    return best % 1000000007;
}

static long seed = 1191;

static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648L;
    return seed / 65536;
}

int main(void) {
    long *arrays[4];
    for (int a = 0; a < 4; a++) {
        arrays[a] = malloc(N * sizeof(long));
    }
    for (long i = 0; i < N; i++) {
        long high = next_random();
        long low = next_random();
        long x = (high * 32768 + low) % 20001 - 10000;
        arrays[0][i] = x;
        arrays[1][i] = x + 300 < 10000 ? x + 300 : 10000;
        arrays[2][i] = -labs(x) - 1;
        arrays[3][i] = i % 2 == 0 ? 10000 - i % 7 : i % 5 - 10000;
    }
    long check = 0;
    for (long r = 0; r < 200; r++) {
        for (int a = 0; a < 4; a++) {
            check = (check * 131 + k_concatenation_max_sum(arrays[a], N, 100000 - r)) % 1000000007;
        }
    }
    printf("200 rounds of 4 arrays of 100000 values: checksum %ld\n", check);
    for (int a = 0; a < 4; a++) {
        free(arrays[a]);
    }
    return 0;
}
