// LeetCode #1216 bench, in C: the ★ arm (the longest palindromic
// subsequence, one row at a time) on 48 strings of 1000 letters drawn
// once from 2, 4, 8 or 26 letters, each asked with k = 200, 400, 600 and
// 800; every answer folded into a checksum.

#include <stdio.h>
#include <stdlib.h>

static long long seed = 1216;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int is_valid_palindrome(const char *b, long long n, long long k) {
    long long *row = calloc(n, sizeof(long long));
    for (long long i = n - 1; i >= 0; i--) {
        row[i] = 1;
        long long diagonal = 0;
        for (long long j = i + 1; j < n; j++) {
            long long below = row[j];
            if (b[i] == b[j]) row[j] = diagonal + 2;
            else row[j] = row[j] > row[j - 1] ? row[j] : row[j - 1];
            diagonal = below;
        }
    }
    int answer = n - row[n - 1] <= k;
    free(row);
    return answer;
}

int main(void) {
    static char texts[48][1000];
    const long long alphabets[4] = {2, 4, 8, 26};
    for (int t = 0; t < 48; t++)
        for (int i = 0; i < 1000; i++) texts[t][i] = (char)('a' + next_random() % alphabets[t % 4]);
    const long long ks[4] = {200, 400, 600, 800};
    long long check = 0;
    int yes = 0;
    for (int t = 0; t < 48; t++)
        for (int q = 0; q < 4; q++) {
            int answer = is_valid_palindrome(texts[t], 1000, ks[q]);
            yes += answer;
            check = (check * 131 + (answer ? 2 : 1) + ks[q]) % 1000000007LL;
        }
    printf("48 strings of 1000 letters, 4 budgets each: %d true, checksum %lld\n", yes, check);
    return 0;
}
