// LeetCode #1256 bench, in C: the ★ arm (`num + 1` in binary with its
// leading 1 taken off, the digits found by halving) on 200000 random
// numbers from 0 to 10^9 drawn once, each encoded 20 times; every
// string's length and middle digit folded into a checksum.

#include <stdio.h>
#include <stdlib.h>

#define COUNT 200000

static long long seed = 1256;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// A new string the caller frees.
static char *encode(long long num, int *len) {
    char digits[64];
    int n = 0;
    long long x = num + 1;
    while (x > 1) {
        digits[n++] = x % 2 == 1 ? '1' : '0';
        x /= 2;
    }
    char *s = malloc(n + 1);
    for (int i = 0; i < n; i++) s[i] = digits[n - 1 - i];
    s[n] = 0;
    *len = n;
    return s;
}

static long long nums[COUNT];

int main(void) {
    for (int i = 0; i < COUNT; i++) {
        long long hi = next_random() * 32768;
        nums[i] = (hi + next_random()) % 1000000001;
    }
    long long check = 0;
    for (int r = 0; r < 20; r++)
        for (int i = 0; i < COUNT; i++) {
            int len;
            char *s = encode(nums[i], &len);
            long long mid = len == 0 ? 0 : (s[len / 2] == '1' ? 2 : 1);
            check = (check * 131 + (long long)len * 3 + mid) % 1000000007;
            free(s);
        }
    printf("20 rounds of 200000 numbers: checksum %lld\n", check);
    return 0;
}
