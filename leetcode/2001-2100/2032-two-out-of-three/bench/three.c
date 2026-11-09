// LeetCode #2032: Two Out of Three -- the ★ arm in C, the same algorithm
// and workload as three.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// writes the answer to a fresh buffer and returns its length
static int64_t two_out_of_three(const int64_t *a, const int64_t *b, const int64_t *c, int64_t n, int64_t **out) {
    int64_t mask[101] = {0};
    for (int64_t i = 0; i < n; i++) mask[a[i]] |= 1;
    for (int64_t i = 0; i < n; i++) mask[b[i]] |= 2;
    for (int64_t i = 0; i < n; i++) mask[c[i]] |= 4;
    int64_t *res = malloc(100 * sizeof(int64_t));
    int64_t len = 0;
    for (int64_t v = 1; v < 101; v++)
        if (__builtin_popcountll((uint64_t)mask[v]) >= 2) res[len++] = v;
    *out = res;
    return len;
}

static int64_t seed = 2032;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t problems[100][3][100];
    for (int64_t p = 0; p < 100; p++)
        for (int k = 0; k < 3; k++)
            for (int i = 0; i < 100; i++) problems[p][k][i] = next_random() % (p % 90 + 11) + 1;
    int64_t calls = 0, kept = 0, check = 0;
    for (int64_t round = 0; round < 4000; round++) {
        for (int64_t p = 0; p < 100; p++) {
            int64_t k = (round + p) % 3;
            int64_t at = (round * 7 + p * 13) % 100;
            problems[p][k][at] = (problems[p][k][at] + round) % 100 + 1;
            int64_t *ans;
            int64_t len = two_out_of_three(problems[p][0], problems[p][1], problems[p][2], 100, &ans);
            calls++;
            kept += len;
            for (int64_t i = 0; i < len; i++) check = (check * 31 + ans[i]) % 1000000007;
            free(ans);
        }
    }
    printf("%lld calls: %lld values kept, checksum %lld\n", (long long)calls, (long long)kept, (long long)check);
    return 0;
}
