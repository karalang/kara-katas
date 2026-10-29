// LeetCode #1010 bench: the ★ arm (remainder counts in one pass) over 20
// playlists of 60,000 songs, drawn once; each of 250 rounds counts the
// pairs of every playlist, starting from a different one, and folds each
// count into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_pairs(const int64_t *time, int64_t n) {
    int64_t seen[60] = {0};
    int64_t pairs = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t r = time[i] % 60;
        pairs += seen[(60 - r) % 60];
        seen[r] += 1;
    }
    return pairs;
}

static int64_t seed = 1010;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 20, ROUNDS = 250, N = 60000 };
    int64_t *playlists = malloc((size_t)COUNT * N * sizeof(int64_t));
    for (int k = 0; k < COUNT; k++)
        for (int i = 0; i < N; i++) playlists[(int64_t)k * N + i] = 1 + next_random() % 500;
    int64_t check = 0;
    for (int64_t r = 0; r < ROUNDS; r++)
        for (int64_t k = 0; k < COUNT; k++)
            check = (check * 31 + num_pairs(playlists + ((r + k) % COUNT) * N, N)) % 1000000007;
    printf("%d rounds over %d playlists of 60000 songs: checksum %lld\n", ROUNDS, COUNT, (long long)check);
    free(playlists);
    return 0;
}
