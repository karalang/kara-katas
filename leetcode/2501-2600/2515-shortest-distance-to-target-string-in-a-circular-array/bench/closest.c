// LeetCode #2515: Shortest Distance to Target String in a Circular Array
// -- C mirror of the benchmark (closest.kara): the same lists, passes,
// order and checksum.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static char words[2000][100][4];

static int64_t closet_target(char (*list)[4], const char *target, int64_t start) {
    const int64_t n = 100;
    int64_t best = -1;
    for (int64_t i = 0; i < n; i++) {
        if (strcmp(list[i], target) == 0) {
            int64_t d = i > start ? i - start : start - i;
            int64_t shortest = d < n - d ? d : n - d;
            if (best == -1 || shortest < best) best = shortest;
        }
    }
    return best;
}

static int64_t seed = 2515;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    for (int l = 0; l < 2000; l++) {
        for (int w = 0; w < 100; w++) {
            int64_t length = next_random() % 3 + 1;
            for (int64_t k = 0; k < length; k++) words[l][w][k] = (char)('a' + next_random() % 3);
            words[l][w][length] = 0;
        }
    }
    const int64_t passes = 900;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int l = 0; l < 2000; l++) {
            char target[4];
            strcpy(target, words[l][check / 100 % 100]);
            check = (check * 31 + closet_target(words[l], target, check % 100) + p) % 1000000007;
        }
    }
    printf("%lld passes over 2000 lists of 100 words: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
