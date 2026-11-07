// LeetCode #2002: Maximum Product of the Length of Two Palindromic
// Subsequences -- the benchmark, the same algorithm as palindromes.kara:
// the picked, left-out and reversed letters and the DP table are heap
// buffers made for each mask, as the Kāra program's are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t longest_palindrome(const unsigned char *chars, int n) {
    if (n == 0) return 0;
    int64_t **dp = malloc(sizeof(int64_t *) * n);
    for (int i = 0; i < n; i++) dp[i] = calloc(n, sizeof(int64_t));
    for (int i = n - 1; i >= 0; i--) {
        dp[i][i] = 1;
        for (int j = i + 1; j < n; j++) {
            if (chars[i] == chars[j]) dp[i][j] = dp[i + 1][j - 1] + 2;
            else dp[i][j] = dp[i + 1][j] > dp[i][j - 1] ? dp[i + 1][j] : dp[i][j - 1];
        }
    }
    int64_t r = dp[0][n - 1];
    for (int i = 0; i < n; i++) free(dp[i]);
    free(dp);
    return r;
}

static int64_t max_product(const char *s) {
    int n = (int)strlen(s);
    int64_t best = 0;
    for (int mask = 1; mask < (1 << n); mask++) {
        unsigned char *picked = malloc(n), *rest = malloc(n), *rev = malloc(n);
        int np = 0, nr = 0;
        for (int i = 0; i < n; i++) {
            if ((mask >> i) & 1) picked[np++] = (unsigned char)s[i];
            else rest[nr++] = (unsigned char)s[i];
        }
        for (int i = 0; i < np; i++) rev[i] = picked[np - 1 - i];
        if (memcmp(picked, rev, np) == 0) {
            int64_t v = np * longest_palindrome(rest, nr);
            if (v > best) best = v;
        }
        free(picked); free(rest); free(rev);
    }
    return best;
}

static int64_t seed = 2002;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char strs[3000][13];
    for (int a = 0; a < 3000; a++) {
        for (int i = 0; i < 12; i++) strs[a][i] = (char)(97 + next_random() % (2 + a % 4));
        strs[a][12] = 0;
    }
    int64_t sum = 0, check = 0;
    for (int a = 0; a < 3000; a++) {
        int64_t answer = max_product(strs[a]);
        sum += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    printf("3000 strings: sum %lld, checksum %lld\n", (long long)sum, (long long)check);
    return 0;
}
