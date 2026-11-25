// LeetCode #1400 bench -- C: at least k letters, and at most k letters
// that appear an odd number of times, the letters counted in an array of
// 26; the string copied for each round as the other languages' are.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int can_construct(const char *s, long long len, int k) {
    if (len < k) return 0;
    long long count[26] = {0};
    for (long long i = 0; i < len; i++) count[(unsigned char)s[i] - 'a']++;
    int odd = 0;
    for (int c = 0; c < 26; c++)
        if (count[c] % 2 == 1) odd++;
    return odd <= k;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const long long n = 100000;
    long long seed = 1400;
    char *letters = malloc(n);
    for (long long i = 0; i < n; i++) letters[i] = (char)(97 + next_random(&seed) % 26);
    long long check = 0;
    for (int r = 0; r < 3000; r++) {
        seed = (seed + check) % 2147483648LL;
        long long at = next_random(&seed) % n;
        letters[at] = (char)(97 + next_random(&seed) % 26);
        long long k = 1 + next_random(&seed) % 30;
        char *s = malloc(n);
        memcpy(s, letters, n);
        int got = can_construct(s, n, (int)k);
        free(s);
        check = (check * 131 + (got ? k : 0) + at) % 1000000007;
    }
    free(letters);
    printf("3000 rounds over 10^5 letters: checksum %lld\n", check);
    return 0;
}
