// LeetCode #1686: Stone Game VI -- the bench's C mirror: the ★ arm on 50
// random games of 100000 stones, all drawn first, each answered 10 times.
// The indexes are malloc'd per answer, as the other languages build a new
// vector.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define SIZE 100000
#define ROUNDS 10

static const int32_t *weight_alice, *weight_bob;

// heaviest first
static int by_weight(const void *x, const void *y) {
    int64_t i = *(const int64_t *)x, j = *(const int64_t *)y;
    int32_t wi = weight_alice[i] + weight_bob[i], wj = weight_alice[j] + weight_bob[j];
    return (wj > wi) - (wj < wi);
}

static int32_t stone_game(const int32_t *alice, const int32_t *bob, int64_t n) {
    int64_t *order = malloc((size_t)n * sizeof *order);
    for (int64_t i = 0; i < n; i++) order[i] = i;
    weight_alice = alice;
    weight_bob = bob;
    qsort(order, (size_t)n, sizeof *order, by_weight);
    int32_t difference = 0;
    for (int64_t turn = 0; turn < n; turn++) {
        int64_t i = order[turn];
        if (turn % 2 == 0) difference += alice[i];
        else difference -= bob[i];
    }
    free(order);
    return (difference > 0) - (difference < 0);
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1686;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t alice[COUNT][SIZE], bob[COUNT][SIZE];
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < SIZE; i++) {
            alice[c][i] = (int32_t)(next_random() % 100 + 1);
            bob[c][i] = (int32_t)(next_random() % 100 + 1);
        }
    }
    int64_t wins[3] = {0, 0, 0}, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int32_t answer = stone_game(alice[c], bob[c], SIZE);
            wins[answer + 1] += 1;
            check = (check * 31 + answer + 2 + r) % 1000000007;
        }
    }
    printf("%d games of %d stones, %d rounds: Alice %lld, Bob %lld, draws %lld, checksum %lld\n", COUNT, SIZE, ROUNDS,
           (long long)wins[2], (long long)wins[0], (long long)wins[1], (long long)check);
    return 0;
}
