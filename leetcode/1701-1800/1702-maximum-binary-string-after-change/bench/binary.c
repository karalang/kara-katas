// LeetCode #1702: Maximum Binary String After Change -- the bench's C
// mirror: the ★ arm on 50 random strings of 100000 digits, all drawn
// first, each answered 40 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 50
#define ROUNDS 40
#define N 100000

// a new string of n digits: one 0 left, at the first 0 plus the zeros less one
static char *maximum_binary_string(const char *binary, int64_t n) {
    int64_t first = -1, zeros = 0;
    for (int64_t i = 0; i < n; i++) {
        if (binary[i] == '0') {
            if (first < 0) {
                first = i;
            }
            zeros++;
        }
    }
    char *out = malloc((size_t)n + 1);
    if (zeros == 0) {
        memcpy(out, binary, (size_t)n + 1);
        return out;
    }
    for (int64_t i = 0; i < n; i++) {
        out[i] = i == first + zeros - 1 ? '0' : '1';
    }
    out[n] = '\0';
    return out;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1702;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    char *strings[COUNT];
    for (int c = 0; c < COUNT; c++) {
        // each digit a 1 with a chance of its string's own, 0 to 10 in 10
        int64_t lean = next_random() % 11;
        strings[c] = malloc(N + 1);
        for (int64_t i = 0; i < N; i++) {
            strings[c][i] = next_random() % 10 < lean ? '1' : '0';
        }
        strings[c][N] = '\0';
    }
    int64_t ones = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            char *answer = maximum_binary_string(strings[c], N);
            // the 0's place, or the length when none is left
            int64_t zero = N;
            for (int64_t i = 0; i < N; i++) {
                if (answer[i] == '0') {
                    zero = i;
                    break;
                }
            }
            ones += N - (zero < N ? 1 : 0);
            check = (check * 31 + answer[check % N] + zero) % 1000000007;
            free(answer);
        }
    }
    printf("%d strings of %d digits, %d rounds: %lld ones, checksum %lld\n", COUNT, N, ROUNDS, (long long)ones, (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(strings[c]);
    }
    return 0;
}
