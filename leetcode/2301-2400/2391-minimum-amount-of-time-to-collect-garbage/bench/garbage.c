// LeetCode #2391: Minimum Amount of Time to Collect Garbage -- the bench,
// the ★ arm in C: the units counted once, each truck driven to the last
// house holding its kind by the travel's prefix sums.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define STREETS 50
#define HOUSES 2000

static int64_t seed = 2391;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t garbage_collection(char **garbage, const int64_t *lens, int64_t n, const int64_t *travel) {
    int64_t minutes = 0;
    int64_t last[3] = {0, 0, 0};
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = 0; j < lens[i]; j++) {
            char b = garbage[i][j];
            minutes++;
            last[b == 'M' ? 0 : b == 'P' ? 1 : 2] = i;
        }
    }
    int64_t *prefix = malloc(sizeof(int64_t) * n);
    prefix[0] = 0;
    for (int64_t i = 1; i < n; i++) prefix[i] = prefix[i - 1] + travel[i - 1];
    for (int kind = 0; kind < 3; kind++) minutes += prefix[last[kind]];
    free(prefix);
    return minutes;
}

int main(void) {
    static char *streets[STREETS][HOUSES];
    static int64_t lens[STREETS][HOUSES];
    static int64_t roads[STREETS][HOUSES - 1];
    for (int s = 0; s < STREETS; s++) {
        for (int h = 0; h < HOUSES; h++) {
            int64_t len = 1 + next_random() % 10;
            streets[s][h] = malloc(len);
            lens[s][h] = len;
            for (int64_t j = 0; j < len; j++) streets[s][h][j] = "MPG"[next_random() % 3];
        }
        for (int h = 0; h < HOUSES - 1; h++) roads[s][h] = 1 + next_random() % 100;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int s = 0; s < STREETS; s++) {
            check = (check * 31 + garbage_collection(streets[s], lens[s], HOUSES, roads[s]) + p) % 1000000007;
        }
    }
    printf("500 passes over 50 streets of 2000 houses: checksum %lld\n", (long long)check);
    for (int s = 0; s < STREETS; s++)
        for (int h = 0; h < HOUSES; h++) free(streets[s][h]);
    return 0;
}
