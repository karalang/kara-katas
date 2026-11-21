// LeetCode #2350: Shortest Impossible Sequence of Rolls -- the bench, the ★
// arm in C: the rolls cut greedily into pieces that each hold every face,
// with a table of the faces seen in the current piece made afresh at its
// end.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t shortest_sequence(const int64_t *rolls, int64_t n, int64_t k) {
    uint8_t *seen = calloc(k + 1, 1);
    int64_t distinct = 0, pieces = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t r = rolls[i];
        if (!seen[r]) {
            seen[r] = 1;
            distinct += 1;
            if (distinct == k) {
                pieces += 1;
                distinct = 0;
                free(seen);
                seen = calloc(k + 1, 1);
            }
        }
    }
    free(seen);
    return pieces + 1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245LL + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 10 arrays of 10^5 rolls, of dice with 2 to 10^4 faces
    int64_t faces[10] = {2, 3, 6, 10, 20, 50, 100, 1000, 3000, 10000};
    int64_t seed = 2350;
    int64_t *arrays[10];
    for (int a = 0; a < 10; a++) {
        arrays[a] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) {
            int64_t high = next_random(&seed);
            arrays[a][i] = (high * 32768 + next_random(&seed)) % faces[a] + 1;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++)
        for (int a = 0; a < 10; a++)
            check = (check * 31 + shortest_sequence(arrays[a], 100000, faces[a]) + p) % 1000000007;
    printf("50 passes over 10 arrays of 10^5 rolls: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) free(arrays[a]);
    return 0;
}
