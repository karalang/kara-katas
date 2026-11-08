// LeetCode #1505: Minimum Possible Integer After at Most K Adjacent Swaps On
// Digits -- the benchmark, the same algorithm as swaps.kara: per-digit
// queues of indices and a Fenwick tree of the digits already taken.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 30000

static int64_t taken_before(const int64_t *tree, int64_t i) {
    int64_t s = 0;
    while (i > 0) { s += tree[i]; i -= i & -i; }
    return s;
}

static void take(int64_t *tree, int64_t len, int64_t i) {
    for (int64_t at = i + 1; at < len; at += at & -at) tree[at]++;
}

static void min_integer(const char *num, int64_t n, int64_t k, char *out) {
    int64_t *wh = malloc(10 * n * sizeof(int64_t));
    int64_t count[10] = {0}, head[10] = {0};
    for (int64_t i = 0; i < n; i++) { int d = num[i] - '0'; wh[d * n + count[d]++] = i; }
    int64_t *tree = calloc(n + 1, sizeof(int64_t));
    int64_t left = k, len = 0;
    for (int64_t r = 0; r < n; r++) {
        for (int d = 0; d < 10; d++) {
            if (head[d] < count[d]) {
                int64_t i = wh[d * n + head[d]];
                int64_t cost = i - taken_before(tree, i);
                if (cost <= left) {
                    left -= cost;
                    head[d]++;
                    take(tree, n + 1, i);
                    out[len++] = (char)('0' + d);
                    break;
                }
            }
        }
    }
    free(wh); free(tree);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1505;
    static char nums[60][N];
    int64_t ks[60];
    for (int c = 0; c < 60; c++) {
        int64_t digits = c % 10 + 1;
        for (int i = 0; i < N; i++) nums[c][i] = (char)(48 + next_random(&seed) % digits);
        ks[c] = next_random(&seed) * (c % 7 + 1) * 50;
    }
    static char out[N];
    int64_t check = 0;
    for (int c = 0; c < 60; c++) {
        min_integer(nums[c], N, ks[c], out);
        for (int i = 0; i < N; i++) check = mix(check, out[i] - 48);
    }
    printf("60 numbers of 30000 digits: checksum %lld\n", (long long)check);
    return 0;
}
