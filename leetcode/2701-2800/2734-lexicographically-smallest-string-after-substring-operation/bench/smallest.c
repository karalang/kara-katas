// LeetCode #2734: Lexicographically Smallest String After Substring
// Operation -- the bench (smallest.kara in C): the run from the first
// letter that is not an 'a' up to the next 'a' moved back a letter, in a
// fresh copy of the bytes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *smallest_string(const char *s, int64_t n) {
    char *b = malloc((size_t)n + 1);
    memcpy(b, s, (size_t)n + 1);
    int64_t i = 0;
    while (i < n && b[i] == 'a') i++;
    if (i == n) {
        b[n - 1] = 'z';
    } else {
        while (i < n && b[i] != 'a') {
            b[i] -= 1;
            i++;
        }
    }
    return b;
}

static int64_t seed = 2734;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 100, rounds = 20;
    const int64_t n = 100000;
    char **words = malloc(sizeof(char *) * count);
    for (int c = 0; c < count; c++) {
        int64_t lead = next_random() % (n / 2);
        char *word = malloc((size_t)n + 1);
        for (int64_t k = 0; k < n; k++) {
            if (k < lead || next_random() % 5000 == 0) word[k] = 'a';
            else word[k] = (char)('b' + next_random() % 25);
        }
        word[n] = 0;
        words[c] = word;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < count; c++) {
            char *b = smallest_string(words[c], n);
            int64_t moved = 0;
            for (int64_t k = 0; k < n; k++) {
                if (b[k] != words[c][k]) moved++;
            }
            sum += moved;
            check = (check * 31 + moved + (b[n / 2] - 'a') + r) % 1000000007;
            free(b);
        }
    }
    printf("%d words of %lld letters, %d rounds: letters moved sum to %lld, checksum %lld\n", count, (long long)n, rounds, (long long)sum, (long long)check);
    for (int c = 0; c < count; c++) free(words[c]);
    free(words);
    return 0;
}
