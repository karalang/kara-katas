// LeetCode #1234 bench: the ★ arm in C, over the same 40 strings of 10^5
// letters and 20 passes as the Kāra bench.
#include <stdio.h>
#include <stdlib.h>

static long index_of(char c) { return c == 'Q' ? 0 : c == 'W' ? 1 : c == 'E' ? 2 : 3; }

static int fits(const long *outside, long k) {
    for (int i = 0; i < 4; i++)
        if (outside[i] > k) return 0;
    return 1;
}

static long balanced_string(const char *s, long n) {
    long k = n / 4;
    long outside[4] = {0, 0, 0, 0};
    for (long i = 0; i < n; i++) outside[index_of(s[i])]++;
    if (outside[0] == k && outside[1] == k && outside[2] == k && outside[3] == k) return 0;
    long best = n, left = 0;
    for (long right = 0; right < n; right++) {
        outside[index_of(s[right])]--;
        while (left <= right && fits(outside, k)) {
            if (right - left + 1 < best) best = right - left + 1;
            outside[index_of(s[left])]++;
            left++;
        }
    }
    return best;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1234;
    char *strings = malloc(40 * 100000);
    for (int t = 0; t < 40; t++) {
        long lean = t % 4;
        for (long i = 0; i < 100000; i++) {
            long r = next_random(&seed) % (4 + lean);
            strings[(long)t * 100000 + i] = r >= 4 || r == 0 ? 'Q' : r == 1 ? 'W' : r == 2 ? 'E' : 'R';
        }
    }
    long check = 0;
    for (int pass = 0; pass < 20; pass++)
        for (int t = 0; t < 40; t++)
            check = (check * 131 + balanced_string(strings + (long)t * 100000, 100000)) % 1000000007;
    printf("40 strings of 10^5 letters, 20 passes: checksum %ld\n", check);
    free(strings);
    return 0;
}
