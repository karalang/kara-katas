// LeetCode #2745: Construct the Longest New String -- the bench
// (longest.kara in C): the table arm, bottom up over the pieces left and
// the last piece placed, flat in one array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_string(int64_t x, int64_t y, int64_t z) {
#define AT(a, b, c, last) ((((a) * (y + 1) + (b)) * (z + 1) + (c)) * 4 + (last))
    int64_t *more = calloc((size_t)((x + 1) * (y + 1) * (z + 1) * 4), sizeof(int64_t));
    for (int64_t a = 0; a <= x; a++)
        for (int64_t b = 0; b <= y; b++)
            for (int64_t c = 0; c <= z; c++)
                for (int64_t last = 0; last < 4; last++) {
                    int64_t best = 0, v;
                    if (a > 0 && last != 0) { v = 2 + more[AT(a - 1, b, c, 0)]; if (v > best) best = v; }
                    if (b > 0 && (last == 0 || last == 3)) { v = 2 + more[AT(a, b - 1, c, 1)]; if (v > best) best = v; }
                    if (c > 0 && last != 0) { v = 2 + more[AT(a, b, c - 1, 2)]; if (v > best) best = v; }
                    more[AT(a, b, c, last)] = best;
                }
    int64_t answer = more[AT(x, y, z, 3)];
#undef AT
    free(more);
    return answer;
}

static int64_t seed = 2745;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 1000, rounds = 3;
    int64_t cases[1000][3];
    for (int k = 0; k < count; k++) {
        cases[k][0] = next_random() % 50 + 1;
        cases[k][1] = next_random() % 50 + 1;
        cases[k][2] = next_random() % 50 + 1;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t length = longest_string(cases[k][0], cases[k][1], cases[k][2]);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    printf("%d counts, %d rounds: lengths sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    return 0;
}
