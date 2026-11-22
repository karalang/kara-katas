// LeetCode #2728: Count Houses in a Circular Street -- the bench in C: the
// ★ arm over 300 streets of up to 1000 houses with k = 1000, all drawn
// first, then each walked 500 times through the judge's street, whose
// moves are counted.
#include <stdint.h>
#include <stdio.h>

#define COUNT 300

static int64_t seed = 2728;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    char doors[1000];
    int64_t n, at, moves;
} Street;

static void open_door(Street *s) { s->doors[s->at] = 1; }
static void close_door(Street *s) { s->doors[s->at] = 0; }
static int is_door_open(const Street *s) { return s->doors[s->at]; }
static void move_right(Street *s) {
    s->at = (s->at + 1) % s->n;
    s->moves++;
}

static int64_t house_count(Street *street, int64_t k) {
    for (int64_t i = 0; i < k; i++) {
        close_door(street);
        move_right(street);
    }
    open_door(street);
    int64_t houses = 1;
    move_right(street);
    while (!is_door_open(street)) {
        houses++;
        move_right(street);
    }
    return houses;
}

static Street streets[COUNT];

int main(void) {
    int rounds = 500;
    for (int c = 0; c < COUNT; c++) {
        int64_t n = next_random() % 1000 + 1;
        streets[c].n = n;
        for (int64_t i = 0; i < n; i++) streets[c].doors[i] = next_random() % 2 == 0;
        streets[c].at = next_random() % n;
        streets[c].moves = 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = house_count(&streets[c], 1000);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    int64_t moves = 0;
    for (int c = 0; c < COUNT; c++) moves += streets[c].moves;
    printf("%d streets, %d rounds: houses sum to %lld in %lld moves, checksum %lld\n", COUNT, rounds, (long long)total, (long long)moves, (long long)check);
    return 0;
}
