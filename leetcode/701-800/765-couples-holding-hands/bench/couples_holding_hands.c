// LeetCode 765 — Couples Holding Hands: benchmark, the ★ arm in C.
// 1,000,000 random rows of 60 seats.
#include <stdint.h>
#include <stdio.h>

static int64_t min_swaps_couples(int64_t *row, int n) {
    int64_t seat_of[60];
    for (int i = 0; i < n; i++) seat_of[row[i]] = i;
    int64_t swaps = 0;
    for (int i = 0; i < n; i += 2) {
        int64_t partner = row[i] ^ 1;
        if (row[i + 1] != partner) {
            int64_t j = seat_of[partner];
            int64_t moved = row[i + 1];
            row[j] = moved;
            seat_of[moved] = j;
            row[i + 1] = partner;
            seat_of[partner] = i + 1;
            swaps++;
        }
    }
    return swaps;
}

static int64_t seed = 765;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 1000000;
    int64_t total = 0, check = 0;
    int64_t row[60];
    for (int r = 0; r < rounds; r++) {
        for (int p = 0; p < 60; p++) row[p] = p;
        for (int i = 0; i < 60; i++) {
            int j = i + (int)(next_random() % (60 - i));
            int64_t t = row[i];
            row[i] = row[j];
            row[j] = t;
        }
        int64_t swaps = min_swaps_couples(row, 60);
        total += swaps;
        check = (check * 31 + swaps) % 1000000007;
    }
    printf("%d rows of 60 seats: %lld swaps in all, checksum %lld\n", rounds, (long long)total, (long long)check);
    return 0;
}
