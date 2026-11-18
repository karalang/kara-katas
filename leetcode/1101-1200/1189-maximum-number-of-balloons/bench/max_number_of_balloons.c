// LeetCode #1189 bench: the ★ arm in C, over the same 200 texts of 10^4
// letters and 200 rounds as the Kāra bench.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROUNDS 200
#define TEXTS 200
#define LETTERS 10000

static long max_number_of_balloons(const char *text, size_t n) {
    long count[26] = {0};
    for (size_t i = 0; i < n; i++) {
        count[(unsigned char)text[i] - 'a']++;
    }
    long words[5] = {count['b' - 'a'], count['a' - 'a'], count['l' - 'a'] / 2,
                     count['o' - 'a'] / 2, count['n' - 'a']};
    long least = words[0];
    for (int k = 1; k < 5; k++) {
        if (words[k] < least) {
            least = words[k];
        }
    }
    return least;
}

static long seed = 1189;

static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648L;
    return seed / 65536;
}

int main(void) {
    const char *alphabets[3] = {"abcdefghijklmnopqrstuvwxyz", "balloon", "balonxy"};
    char *texts[TEXTS];
    for (int i = 0; i < TEXTS; i++) {
        const char *pool = alphabets[i % 3];
        long len = (long)strlen(pool);
        texts[i] = malloc(LETTERS);
        for (int j = 0; j < LETTERS; j++) {
            texts[i][j] = pool[next_random() % len];
        }
    }
    long check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int i = 0; i < TEXTS; i++) {
            check = (check * 131 + max_number_of_balloons(texts[i], LETTERS) + 1) % 1000000007;
        }
    }
    printf("%d rounds of %d texts of %d letters: checksum %ld\n", ROUNDS, TEXTS, LETTERS, check);
    for (int i = 0; i < TEXTS; i++) {
        free(texts[i]);
    }
    return 0;
}
