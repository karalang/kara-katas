// LeetCode #2027: Minimum Moves to Convert String -- the ★ arm in C, the same
// algorithm and workload as moves.kara: the string copied into a fresh
// array of chars, then a move at the leftmost X and a jump of three.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t minimum_moves(const char *s, int64_t n) {
    char *key = malloc(n);
    memcpy(key, s, n);
    int64_t moves = 0;
    int64_t i = 0;
    while (i < n) {
        if (key[i] == 'X') {
            moves++;
            i += 3;
        } else {
            i++;
        }
    }
    free(key);
    return moves;
}

static int64_t seed = 2027;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char strings[2000][1000];
    for (int a = 0; a < 2000; a++) {
        int64_t share = next_random() % 101;
        for (int i = 0; i < 1000; i++) strings[a][i] = next_random() % 100 < share ? 'X' : 'O';
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int r = 0; r < 50; r++) {
        for (int a = 0; a < 2000; a++) {
            int64_t moves = minimum_moves(strings[a], 1000);
            calls++;
            total += moves;
            check = (check * 31 + moves) % 1000000007;
        }
    }
    printf("%lld calls: %lld moves, checksum %lld\n", (long long)calls, (long long)total, (long long)check);
    return 0;
}
