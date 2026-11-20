// LeetCode #1223 bench, C mirror of the Kāra ★ arm: count the sequences by
// their last face and run length, for 50 random sets of limits at
// n = 5000; checksum of the answers.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 1223;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t die_simulator(int64_t n, const int64_t *roll_max) {
    const int64_t modulus = 1000000007;
    int64_t (*count)[15] = calloc(6, sizeof *count);
    for (int f = 0; f < 6; f++) {
        count[f][0] = 1;
    }
    for (int64_t step = 1; step < n; step++) {
        int64_t (*next)[15] = calloc(6, sizeof *next);
        for (int f = 0; f < 6; f++) {
            for (int64_t r = 0; r < roll_max[f]; r++) {
                int64_t c = count[f][r];
                if (c == 0) {
                    continue;
                }
                for (int g = 0; g < 6; g++) {
                    if (g != f) {
                        next[g][0] = (next[g][0] + c) % modulus;
                    } else if (r + 1 < roll_max[f]) {
                        next[f][r + 1] = (next[f][r + 1] + c) % modulus;
                    }
                }
            }
        }
        free(count);
        count = next;
    }
    int64_t total = 0;
    for (int f = 0; f < 6; f++) {
        for (int r = 0; r < 15; r++) {
            total = (total + count[f][r]) % modulus;
        }
    }
    free(count);
    return total;
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 50; t++) {
        int64_t roll_max[6];
        for (int f = 0; f < 6; f++) {
            roll_max[f] = next_random() % 15 + 1;
        }
        check = (check * 131 + die_simulator(5000, roll_max)) % 1000000007;
    }
    printf("50 sets of limits at n = 5000: checksum %lld\n", (long long)check);
    return 0;
}
