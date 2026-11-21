// LeetCode #2484: Count Palindromic Subsequences -- bench, C mirror of
// palin.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define MOD 1000000007LL

static int64_t count_palindromes(const char *s) {
    int64_t n = (int64_t)strlen(s);
    int64_t before_one[10] = {0}, before_two[100] = {0}, after_one[10] = {0}, after_two[100] = {0};
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t d = s[i] - '0';
        for (int a = 0; a < 10; a++) after_two[d * 10 + a] += after_one[a];
        after_one[d] += 1;
    }
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t d = s[i] - '0';
        after_one[d] -= 1;
        for (int a = 0; a < 10; a++) after_two[d * 10 + a] -= after_one[a];
        int64_t here = 0;
        for (int a = 0; a < 10; a++)
            for (int b = 0; b < 10; b++) here += before_two[a * 10 + b] * after_two[b * 10 + a];
        total = (total + here) % MOD;
        for (int a = 0; a < 10; a++) before_two[a * 10 + d] += before_one[a];
        before_one[d] += 1;
    }
    return total;
}

static int64_t seed = 2484;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t strings[4][2000];
    for (int g = 0; g < 4; g++)
        for (int i = 0; i < 2000; i++) strings[g][i] = next_random() % 10;
    char s[2001];
    int64_t check = 0;
    for (int64_t p = 0; p < 110; p++) {
        for (int g = 0; g < 4; g++) {
            strings[g][check % 2000] = check / 2000 % 10;
            for (int i = 0; i < 2000; i++) s[i] = (char)('0' + strings[g][i]);
            s[2000] = 0;
            check = (check * 31 + count_palindromes(s) + p) % MOD;
        }
    }
    printf("110 passes over 4 strings of 2000 digits: checksum %lld\n", (long long)check);
    return 0;
}
