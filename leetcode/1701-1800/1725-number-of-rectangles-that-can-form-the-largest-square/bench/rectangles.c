// LeetCode #1725: Number Of Rectangles That Can Form The Largest Square
// -- the bench (rectangles.kara): one pass, the largest shorter side so
// far and how many rectangles give it.
//
// Each rectangle a pair of int32_t in one flat array, where Kāra, Rust
// and Go hold a list of two-element lists.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 1000
#define ROUNDS 50
#define N 1000

static int32_t count_good_rectangles(const int32_t (*rectangles)[2], int n) {
    int32_t best = 0;
    int32_t count = 0;
    for (int i = 0; i < n; i++) {
        int32_t side = rectangles[i][0] < rectangles[i][1] ? rectangles[i][0] : rectangles[i][1];
        if (side > best) {
            best = side;
            count = 1;
        } else if (side == best) {
            count++;
        }
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    static int32_t problems[COUNT][N][2];
    int64_t seed = 1725;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) {
            problems[c][i][0] = (int32_t)(next_random(&seed) % 20 + 1);
            problems[c][i][1] = (int32_t)(next_random(&seed) % 20 + 1);
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = count_good_rectangles((const int32_t (*)[2])problems[c], N);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d rectangles, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)sum, (long long)check);
    return 0;
}
