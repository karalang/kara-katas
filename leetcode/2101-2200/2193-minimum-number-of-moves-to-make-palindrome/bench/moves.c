// benchmark's C mirror of moves.kara (LeetCode #2193, the ★ arm): the
// twin swapped out to the end, over a copy of the word's bytes.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long min_moves(const char *s, long long n, char *b) {
    memcpy(b, s, n);
    long long left = 0, right = n - 1, moves = 0;
    while (left < right) {
        long long k = right;
        while (k > left && b[k] != b[left]) k--;
        if (k == left) {
            char t = b[left];
            b[left] = b[left + 1];
            b[left + 1] = t;
            moves++;
            continue;
        }
        while (k < right) {
            char t = b[k];
            b[k] = b[k + 1];
            b[k + 1] = t;
            k++;
            moves++;
        }
        left++;
        right--;
    }
    return moves;
}

static long long seed = 2193;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char words[20][2000];
    for (int w = 0; w < 20; w++) {
        for (int i = 0; i < 1000; i++) {
            char c = (char)(97 + next_random() % 26);
            words[w][2 * i] = c;
            words[w][2 * i + 1] = c;
        }
        for (int i = 1999; i >= 1; i--) {
            long long j = next_random() % (i + 1);
            char t = words[w][i];
            words[w][i] = words[w][j];
            words[w][j] = t;
        }
    }
    char *b = malloc(2000);
    long long check = 0;
    for (int r = 0; r < 3000; r++) check = (check * 31 + min_moves(words[r % 20], 2000, b)) % 1000000007;
    printf("3000 solves: checksum %lld\n", check);
    free(b);
    return 0;
}
