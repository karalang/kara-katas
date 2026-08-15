/* LeetCode 276 bench mirror — brute-force enumeration, C.
 *
 * Same algorithm as paint_enum.kara: split on the first two posts, odometer the
 * suffix, check the whole array for three-in-a-row. Sequential: the 16 prefixes
 * run in a plain loop. */
#include <stdio.h>
#include <stdint.h>

#define N 13
#define K 4

static int64_t count_prefix(int p0, int p1) {
    int c[N] = {0};
    c[0] = p0;
    c[1] = p1;
    int64_t count = 0;
    for (;;) {
        int ok = 1;
        for (int i = 2; i < N; i++)
            if (c[i] == c[i - 1] && c[i - 1] == c[i - 2]) ok = 0;
        if (ok) count++;
        int p = N - 1;
        while (p >= 2 && c[p] == K - 1) { c[p] = 0; p--; }
        if (p < 2) break;
        c[p]++;
    }
    return count;
}

int main(void) {
    int64_t total = 0;
    for (int pre = 0; pre < K * K; pre++)
        total += count_prefix(pre / K, pre % K);
    printf("%lld\n", (long long)total);
    return 0;
}
