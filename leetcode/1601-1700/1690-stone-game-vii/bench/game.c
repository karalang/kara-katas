// LeetCode #1690: Stone Game VII -- the bench's C mirror: the ★ arm on 40
// random rows of 1000 stones, all drawn first, each answered 4 times. The
// two vectors are malloc'd per answer, as the other languages build them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 40
#define SIZE 1000
#define ROUNDS 4

static int32_t stone_game(const int32_t *stones, int64_t n) {
    int32_t *prefix = calloc((size_t)n + 1, sizeof *prefix);
    for (int64_t i = 0; i < n; i++) prefix[i + 1] = prefix[i] + stones[i];
    int32_t *best = calloc((size_t)n, sizeof *best);
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t j = i + 1; j < n; j++) {
            int32_t take_left = prefix[j + 1] - prefix[i + 1] - best[j];
            int32_t take_right = prefix[j] - prefix[i] - best[j - 1];
            best[j] = take_left > take_right ? take_left : take_right;
        }
    }
    int32_t answer = best[n - 1];
    free(prefix);
    free(best);
    return answer;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1690;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t rows[COUNT][SIZE];
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < SIZE; i++) rows[c][i] = (int32_t)(next_random() % 1000 + 1);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int32_t answer = stone_game(rows[c], SIZE);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d rows of %d stones, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, SIZE, ROUNDS, (long long)total, (long long)check);
    return 0;
}
