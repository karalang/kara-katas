// LeetCode #1347 bench -- C: one count per letter, up for s and down for
// t, the positive counts summed.
#include <stdio.h>
#include <string.h>

static char text[1000001];

static int min_steps(const char *s, const char *t, long n) {
    int count[26];
    memset(count, 0, sizeof count);
    for (long i = 0; i < n; i++) count[s[i] - 'a']++;
    for (long i = 0; i < n; i++) count[t[i] - 'a']--;
    int steps = 0;
    for (int c = 0; c < 26; c++)
        if (count[c] > 0) steps += count[c];
    return steps;
}

int main(void) {
    long long seed = 1347;
    for (long i = 0; i < 1000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        text[i] = (char)('a' + (seed / 65536) % 26);
    }
    long long check = 0;
    for (long long q = 0; q < 1000; q++) {
        long long n = 40000 + check % 10001;
        long long a = check % (1000000 - n);
        long long b = (check / 7) % (1000000 - n);
        int steps = min_steps(text + a, text + b, n);
        check = (check * 31 + steps + q) % 1000000007;
    }
    printf("1000 queries over a text of 10^6: checksum %lld\n", check);
    return 0;
}
