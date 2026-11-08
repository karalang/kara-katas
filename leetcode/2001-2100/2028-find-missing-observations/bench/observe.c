// LeetCode #2028: Find Missing Observations -- the ★ arm in C, the same
// algorithm and workload as observe.kara: a fresh array of the even spread.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *missing_rolls(const int64_t *rolls, int64_t m, int64_t mean, int64_t n, int64_t *len) {
    int64_t sum = 0;
    for (int64_t i = 0; i < m; i++) sum += rolls[i];
    int64_t need = mean * (m + n) - sum;
    if (need < n || need > 6 * n) {
        *len = 0;
        return NULL;
    }
    int64_t q = need / n, r = need % n;
    int64_t *out = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) out[i] = i < r ? q + 1 : q;
    *len = n;
    return out;
}

static int64_t seed = 2028;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t lists[20][100000];
    int64_t means[20], ns[20];
    for (int a = 0; a < 20; a++) {
        for (int i = 0; i < 100000; i++) lists[a][i] = next_random() % 6 + 1;
        means[a] = next_random() % 4 + 2;
        ns[a] = next_random() % 100000 + 1;
    }
    int64_t calls = 0, rolls = 0, check = 0;
    for (int round = 0; round < 50; round++) {
        for (int a = 0; a < 20; a++) {
            int64_t len;
            int64_t *got = missing_rolls(lists[a], 100000, means[a], ns[a], &len);
            calls++;
            rolls += len;
            if (len > 0) {
                check = (check * 31 + got[0] * 7 + got[len - 1]) % 1000000007;
            } else {
                check = (check * 31 + 1) % 1000000007;
            }
            free(got);
        }
    }
    printf("%lld calls: %lld rolls, checksum %lld\n", (long long)calls, (long long)rolls, (long long)check);
    return 0;
}
