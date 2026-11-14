// LeetCode #1155 bench -- mirrors num_rolls_to_target.kara: the same 64
// problems, the same passes, the ★ arm's rolling counts.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t num_rolls_to_target(int64_t n, int64_t k, int64_t target) {
    const int64_t modulus = 1000000007;
    int64_t *ways = calloc(target + 1, sizeof(int64_t));
    ways[0] = 1;
    for (int64_t d = 0; d < n; d++) {
        int64_t *next = calloc(target + 1, sizeof(int64_t));
        for (int64_t s = 0; s < target + 1; s++) {
            if (ways[s] != 0) {
                for (int64_t face = 1; face < k + 1; face++) {
                    if (s + face > target) break;
                    next[s + face] = (next[s + face] + ways[s]) % modulus;
                }
            }
        }
        free(ways);
        ways = next;
    }
    int64_t answer = ways[target];
    free(ways);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t passes = 250;
    int64_t seed = 1155;
    int64_t problems[64][3];
    for (int i = 0; i < 64; i++) {
        int64_t n = 1 + next_random(&seed) % 30;
        int64_t k = 1 + next_random(&seed) % 30;
        int64_t most = n * k < 1000 ? n * k : 1000;
        problems[i][0] = n;
        problems[i][1] = k;
        problems[i][2] = n + next_random(&seed) % (most - n + 1);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int i = 0; i < 64; i++)
            check = (check * 31 + num_rolls_to_target(problems[i][0], problems[i][1], problems[i][2]) + p) % 1000000007;
    printf("%lld passes over 64 problems: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
