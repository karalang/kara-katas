// LeetCode #2182: Construct String With Repeat Limit -- the benchmark's C
// mirror of repeat_limit.kara, over a pointer and a length; the result is
// a malloc'd buffer the caller frees.

#include <stdio.h>
#include <stdlib.h>

static char *repeat_limited_string(const char *s, long long n, long long repeat_limit, long long *out_len) {
    long long counts[26] = {0};
    for (long long i = 0; i < n; i++) counts[s[i] - 97]++;
    char *out = malloc(n + 1);
    long long len = 0;
    long long big = 25;
    for (;;) {
        while (big >= 0 && counts[big] == 0) big--;
        if (big < 0) break;
        long long take = counts[big] < repeat_limit ? counts[big] : repeat_limit;
        for (long long t = 0; t < take; t++) out[len++] = (char)(97 + big);
        counts[big] -= take;
        if (counts[big] == 0) continue;
        long long small = big - 1;
        while (small >= 0 && counts[small] == 0) small--;
        if (small < 0) break;
        out[len++] = (char)(97 + small);
        counts[small]--;
    }
    *out_len = len;
    return out;
}

static long long seed = 2182;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char *row = malloc(1000000);
    for (int i = 0; i < 1000000; i++) row[i] = (char)(97 + next_random() % 26);
    long long check = 0;
    for (int r = 0; r < 400; r++) {
        long long a = next_random();
        long long b = next_random();
        long long start = (a * 32768 + b) % 900001;
        long long k = next_random() % 3 + 1;
        long long len;
        char *t = repeat_limited_string(row + start, 100000, k, &len);
        for (long long i = 0; i < len; i++) check = (check * 31 + (unsigned char)t[i]) % 1000000007;
        free(t);
    }
    printf("400 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
