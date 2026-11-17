// LeetCode #2225: Find Players With Zero or One Losses -- the benchmark's
// C mirror of players.kara; the map of losses is an open-addressing hash
// table, C having none of its own, and both lists are sorted by qsort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000
#define SLOTS 524288 /* a power of two, over twice the 2N players a match list can name */

static int64_t keys[SLOTS];
static char used[SLOTS];
static int64_t losses[SLOTS];

static uint64_t slot_of(int64_t key) {
    uint64_t x = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (x ^ (x >> 29)) & (SLOTS - 1);
}

static uint64_t find(int64_t key) {
    uint64_t s = slot_of(key);
    while (used[s] && keys[s] != key) s = (s + 1) & (SLOTS - 1);
    return s;
}

static int by_value(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// fills unbeaten and once (each room for 2n) and their lengths
static void find_winners(int64_t (*matches)[2], int64_t n, int64_t *unbeaten, int64_t *nu,
                         int64_t *once, int64_t *no) {
    for (int i = 0; i < SLOTS; i++) used[i] = 0;
    for (int64_t i = 0; i < n; i++) {
        uint64_t s = find(matches[i][0]);
        if (!used[s]) {
            used[s] = 1;
            keys[s] = matches[i][0];
            losses[s] = 0;
        }
        s = find(matches[i][1]);
        if (!used[s]) {
            used[s] = 1;
            keys[s] = matches[i][1];
            losses[s] = 0;
        }
        losses[s]++;
    }
    *nu = 0;
    *no = 0;
    for (int i = 0; i < SLOTS; i++) {
        if (!used[i]) continue;
        if (losses[i] == 0) unbeaten[(*nu)++] = keys[i];
        else if (losses[i] == 1) once[(*no)++] = keys[i];
    }
    qsort(unbeaten, (size_t)*nu, sizeof(int64_t), by_value);
    qsort(once, (size_t)*no, sizeof(int64_t), by_value);
}

static int64_t seed = 2225;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

// a match between two players of 1 to 10^5, never one against itself
static void draw_match(int64_t *game) {
    int64_t winner = wide_random() % 100000 + 1;
    int64_t loser = wide_random() % 100000 + 1;
    if (loser == winner) loser = winner % 100000 + 1;
    game[0] = winner;
    game[1] = loser;
}

int main(void) {
    int64_t (*tournaments[4])[2];
    for (int t = 0; t < 4; t++) {
        tournaments[t] = malloc(sizeof(int64_t[2]) * N);
        for (int64_t i = 0; i < N; i++) draw_match(tournaments[t][i]);
    }
    int64_t *lists[2] = {malloc(sizeof(int64_t) * 2 * N), malloc(sizeof(int64_t) * 2 * N)};
    int64_t lens[2];
    int64_t listed = 0, check = 0;
    for (int r = 0; r < 25; r++) {
        for (int t = 0; t < 4; t++) {
            // punch: one match is drawn again before each answer
            int64_t at = wide_random() % N;
            draw_match(tournaments[t][at]);
            find_winners(tournaments[t], N, lists[0], &lens[0], lists[1], &lens[1]);
            for (int l = 0; l < 2; l++) {
                listed += lens[l];
                check = (check * 31 + lens[l]) % 1000000007;
                for (int64_t i = 0; i < lens[l]; i++) check = (check * 31 + lists[l][i]) % 1000000007;
            }
        }
    }
    printf("100 tournaments: %lld players listed in all, checksum %lld\n", (long long)listed, (long long)check);
    for (int t = 0; t < 4; t++) free(tournaments[t]);
    free(lists[0]);
    free(lists[1]);
    return 0;
}
