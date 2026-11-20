// LeetCode #1739: Building Boxes -- the bench (boxes.kara in C): the
// staircase layer by layer, then the floor a box at a time.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int minimum_boxes(int n32) {
    int64_t n = n32;
    int64_t placed = 0, side = 0;
    while (placed + (side + 1) * (side + 2) / 2 <= n) {
        side += 1;
        placed += side * (side + 1) / 2;
    }
    int64_t floor = side * (side + 1) / 2, extra = 0;
    while (placed < n) {
        extra += 1;
        floor += 1;
        placed += extra;
    }
    return (int)floor;
}

static int64_t seed = 1739;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int count = 20000, rounds = 15;
    int *counts = malloc(sizeof(int) * count);
    for (int i = 0; i < count; i++) counts[i] = (int)(wide() % 1000000000 + 1);
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            int64_t answer = minimum_boxes(counts[i]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d counts up to 1000000000, %d rounds: floors sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(counts);
    return 0;
}
