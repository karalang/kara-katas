// LeetCode #696: Count Binary Substrings -- bench program, C mirror of the ★ arm.
#include <stdio.h>
#include <stdlib.h>

#define LEN 100000

static long long seed = 696;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long min(long long a, long long b) { return a < b ? a : b; }

static long long count_binary_substrings(const char *s, int n) {
    long long before = 0, current = 1, count = 0;
    for (int i = 1; i < n; i++) {
        if (s[i] == s[i - 1]) {
            current++;
        } else {
            count += min(before, current);
            before = current;
            current = 1;
        }
    }
    return count + min(before, current);
}

int main(void) {
    static char strings[20][LEN];
    for (int k = 0; k < 20; k++) {
        long long longest = 1 + 2 * k;
        int len = 0, bit = 0;
        while (len < LEN) {
            long long run = 1 + next_random() % longest;
            for (long long r = 0; r < run; r++)
                if (len < LEN) strings[k][len++] = bit ? '1' : '0';
            bit = 1 - bit;
        }
    }
    int rounds = 150;
    long long total = 0, checksum = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < 20; k++) {
            long long c = count_binary_substrings(strings[k], LEN);
            total += c;
            checksum = (checksum * 31 + c) % 1000000007;
        }
    printf("%d rounds of 20 strings of 100000: %lld substrings counted, checksum %lld\n", rounds, total, checksum);
    return 0;
}
