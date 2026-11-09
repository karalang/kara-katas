// LeetCode #1079 bench: the C mirror of tiles.kara, the same walk over
// an int64_t[26] of counts and the same workload.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t sequences(int64_t *counts) {
    int64_t total = 0;
    for (int letter = 0; letter < 26; letter++) {
        if (counts[letter] > 0) {
            counts[letter] -= 1;
            total += 1 + sequences(counts);
            counts[letter] += 1;
        }
    }
    return total;
}

static int64_t num_tile_possibilities(const char *tiles) {
    int64_t counts[26] = {0};
    for (const char *p = tiles; *p; p++) {
        counts[*p - 'A'] += 1;
    }
    return sequences(counts);
}

static int64_t seed = 1079;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 200;
    enum { N = 200 };
    static char sets[N][8];
    for (int s = 0; s < N; s++) {
        int64_t d = next_random() % 7 + 1;
        char alphabet[7];
        int have = 0;
        while (have < d) {
            char c = (char)('A' + next_random() % 26);
            if (!memchr(alphabet, c, have)) {
                alphabet[have++] = c;
            }
        }
        for (int i = 0; i < 7; i++) {
            sets[s][i] = alphabet[next_random() % d];
        }
        sets[s][7] = 0;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int j = 0; j < N; j++) {
            int64_t count = num_tile_possibilities(sets[(j * 7 + r) % N]);
            total += count;
            check = (check * 31 + count) % 1000000007;
        }
    }
    printf("%d rounds of %d sets of 7 tiles: %lld sequences, checksum %lld\n", rounds, N, (long long)total, (long long)check);
    return 0;
}
