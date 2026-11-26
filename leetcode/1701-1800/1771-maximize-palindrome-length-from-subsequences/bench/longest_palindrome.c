// LeetCode #1771: Maximize Palindrome Length From Subsequences -- the bench
// in C, mirroring longest_palindrome.kara: the longest palindromic
// subsequence of every stretch of the two words joined, a new table of rows
// each call.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int longest_palindrome(const char *word1, const char *word2) {
    int split = (int)strlen(word1), n = split + (int)strlen(word2);
    char *s = malloc(n + 1);
    memcpy(s, word1, split);
    memcpy(s + split, word2, n - split + 1);
    int **dp = malloc(n * sizeof(int *));
    for (int i = 0; i < n; i++) dp[i] = calloc(n, sizeof(int));
    int best = 0;
    for (int i = n - 1; i >= 0; i--) {
        dp[i][i] = 1;
        for (int j = i + 1; j < n; j++) {
            if (s[i] == s[j]) {
                dp[i][j] = dp[i + 1][j - 1] + 2;
                if (i < split && j >= split && dp[i][j] > best) best = dp[i][j];
            } else {
                int x = dp[i + 1][j], y = dp[i][j - 1];
                dp[i][j] = x > y ? x : y;
            }
        }
    }
    for (int i = 0; i < n; i++) free(dp[i]);
    free(dp);
    free(s);
    return best;
}

static long long seed = 1771;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char words[100][1001];
    for (int w = 0; w < 100; w++) {
        long long letters = 2 + next_random() % 25;
        for (int i = 0; i < 1000; i++) words[w][i] = (char)(97 + next_random() % letters);
        words[w][1000] = 0;
    }
    long long check = 0;
    for (long long call = 0; call < 40; call++) {
        long long a = (check + call * 7919) % 100;
        long long b = (check / 100 + call * 31 + 1) % 100;
        check = (check * 31 + longest_palindrome(words[a], words[b])) % 1000000007;
    }
    printf("40 calls over 100 words: checksum %lld\n", check);
    return 0;
}
