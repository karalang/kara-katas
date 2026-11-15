// LeetCode #2186: Minimum Number of Steps to Make Two Strings Anagram II
// -- the benchmark's C mirror of anagram_steps.kara, over pointers and
// lengths: one balance of 26 counts.

#include <stdio.h>
#include <stdlib.h>

static long long min_steps(const char *s, long long n, const char *t, long long m) {
    long long balance[26] = {0};
    for (long long i = 0; i < n; i++) balance[s[i] - 97]++;
    for (long long i = 0; i < m; i++) balance[t[i] - 97]--;
    long long steps = 0;
    for (int c = 0; c < 26; c++) steps += balance[c] < 0 ? -balance[c] : balance[c];
    return steps;
}

static long long seed = 2186;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char *row = malloc(1000000);
    for (int i = 0; i < 1000000; i++) row[i] = (char)(97 + next_random() % 26);
    long long check = 0;
    for (int r = 0; r < 200; r++) {
        long long a = next_random();
        long long b = next_random();
        long long c = next_random();
        long long d = next_random();
        long long i = (a * 32768 + b) % 800001;
        long long j = (c * 32768 + d) % 800001;
        long long steps = min_steps(row + i, 200000, row + j, 200000);
        check = (check * 31 + steps) % 1000000007;
    }
    printf("200 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
