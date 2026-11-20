// LeetCode #1732: Find the Highest Altitude -- the bench (altitude.kara):
// the altitudes listed, then the largest.
//
// The list of altitudes is a malloc'd array of n + 1, where Kāra, Rust
// and Go push onto a growable list from one element.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 1000
#define ROUNDS 2000
#define N 100

static int32_t largest_altitude(const int32_t *gain, int n) {
    int32_t *altitudes = malloc((size_t)(n + 1) * sizeof(int32_t));
    altitudes[0] = 0;
    for (int i = 0; i < n; i++) {
        altitudes[i + 1] = altitudes[i] + gain[i];
    }
    int32_t highest = altitudes[0];
    for (int i = 1; i <= n; i++) {
        if (altitudes[i] > highest) {
            highest = altitudes[i];
        }
    }
    free(altitudes);
    return highest;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    static int32_t trips[COUNT][N];
    int64_t seed = 1732;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) {
            trips[c][i] = (int32_t)(next_random(&seed) % 201 - 100);
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = largest_altitude(trips[c], N);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d trips of %d gains, %d rounds: highest points sum to %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)sum, (long long)check);
    return 0;
}
