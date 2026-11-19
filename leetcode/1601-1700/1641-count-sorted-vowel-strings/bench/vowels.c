// LeetCode #1641: Count Sorted Vowel Strings -- the bench's C mirror: the
// ★ arm on 4000000 random n from 1 to 50, all drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { DRAWS = 4000000 };

static int64_t count_vowel_strings(int64_t n) {
    int64_t ending[5] = {1, 1, 1, 1, 1};
    for (int64_t i = 1; i < n; i++)
        for (int v = 1; v < 5; v++) ending[v] += ending[v - 1];
    return ending[0] + ending[1] + ending[2] + ending[3] + ending[4];
}

static int64_t seed = 1641;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *ns = malloc(sizeof(int64_t) * DRAWS);
    for (int i = 0; i < DRAWS; i++) ns[i] = next_random() % 50 + 1;
    int64_t check = 0, total = 0;
    for (int i = 0; i < DRAWS; i++) {
        int64_t count = count_vowel_strings(ns[i]);
        total += count;
        check = (check * 31 + count) % 1000000007;
    }
    free(ns);
    printf("4000000 random n: counts sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
