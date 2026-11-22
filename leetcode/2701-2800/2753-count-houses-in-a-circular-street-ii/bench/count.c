// LeetCode #2753: Count Houses in a Circular Street II -- the bench in C:
// the ★ arm over 30 streets of up to 10^5 houses with k = 10^5, all
// drawn first, then each walked 20 times, every walk on a fresh copy of
// its street, the walk closing the doors it meets.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 30
#define K 100000

static int64_t seed = 2753;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    char *doors;
    int64_t n, at, moves;
} Street;

static void close_door(Street *s) { s->doors[s->at] = 0; }
static int is_door_open(const Street *s) { return s->doors[s->at]; }
static void move_right(Street *s) {
    s->at = (s->at + 1) % s->n;
    s->moves++;
}

static int64_t house_count(Street *street, int64_t k) {
    while (!is_door_open(street)) move_right(street);
    int64_t last = 0;
    for (int64_t step = 1; step <= k; step++) {
        move_right(street);
        if (is_door_open(street)) {
            close_door(street);
            last = step;
        }
    }
    return last;
}

static char doors_[COUNT][K];
static int64_t sizes[COUNT], starts[COUNT];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++) {
        int64_t n = next_random() % K + 1;
        sizes[c] = n;
        for (int64_t i = 0; i < n; i++) doors_[c][i] = next_random() % 2 == 0;
        doors_[c][next_random() % n] = 1;
        starts[c] = next_random() % n;
    }
    char *copy = malloc(K);
    int64_t total = 0, moves = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            memcpy(copy, doors_[c], sizes[c]);
            Street street = {copy, sizes[c], starts[c], 0};
            int64_t a = house_count(&street, K);
            total += a;
            moves += street.moves;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    free(copy);
    printf("%d streets, %d rounds: houses sum to %lld in %lld moves, checksum %lld\n", COUNT, rounds, (long long)total, (long long)moves, (long long)check);
    return 0;
}
