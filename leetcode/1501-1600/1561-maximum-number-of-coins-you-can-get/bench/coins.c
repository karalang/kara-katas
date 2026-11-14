// LeetCode #1561: Maximum Number of Coins You Can Get -- bench: the ★ arm
// (sorted, every other pile past the n smallest) over 20 lists of 99999
// piles of 1 to 10000 coins, built once, each asked 10 times.
// C mirror of coins.kara; the copy is sorted by qsort, as C's library sort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 99999

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t max_coins(const int64_t *piles, int64_t len) {
    int64_t *sorted = malloc(len * sizeof(int64_t));
    memcpy(sorted, piles, len * sizeof(int64_t));
    qsort(sorted, len, sizeof(int64_t), cmp);
    int64_t n = len / 3, sum = 0;
    for (int64_t i = n; i < len; i += 2) sum += sorted[i];
    free(sorted);
    return sum;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1561;
    static int64_t lists[20][N];
    for (int l = 0; l < 20; l++)
        for (int i = 0; i < N; i++) lists[l][i] = next_random(&seed) % 10000 + 1;
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 10; pass++) {
        for (int l = 0; l < 20; l++) {
            int64_t coins = max_coins(lists[l], N);
            total += coins;
            check = mix(check, coins);
        }
    }
    printf("10 passes over 20 lists of 99999 piles: %lld coins, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
