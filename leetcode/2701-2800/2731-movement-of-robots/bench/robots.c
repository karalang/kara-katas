// LeetCode #2731: Movement of Robots -- the bench (robots.kara in C): the
// places after d seconds, robots passing through each other in effect,
// sorted by qsort, each adding its distance to all those before it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t sum_distance(const int64_t *nums, const char *s, int64_t n, int64_t d, int64_t *places) {
    for (int64_t i = 0; i < n; i++) places[i] = s[i] == 'L' ? nums[i] - d : nums[i] + d;
    qsort(places, (size_t)n, sizeof(int64_t), cmp);
    int64_t total = 0, before = 0;
    for (int64_t k = 0; k < n; k++) {
        total = (total + k * places[k] - before) % MOD;
        before += places[k];
    }
    return total;
}

static int64_t seed = 2731;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int cases = 10, rounds = 10;
    const int64_t n = 100000;
    int64_t *nums = malloc(sizeof(int64_t) * n * cases);
    char *ways = malloc((size_t)(n * cases));
    int64_t ds[10];
    for (int c = 0; c < cases; c++) {
        int64_t *p = nums + c * n;
        int64_t at = -2000000000LL;
        for (int64_t i = 0; i < n; i++) {
            p[i] = at;
            at += wide() % 40000 + 1;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = p[i]; p[i] = p[j]; p[j] = t;
        }
        for (int64_t i = 0; i < n; i++) ways[c * n + i] = next_random() % 2 == 0 ? 'L' : 'R';
        int64_t hi = next_random();
        ds[c] = (hi * 32768 + next_random()) % 1000000001;
    }
    int64_t *places = malloc(sizeof(int64_t) * n);
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < cases; c++) {
            int64_t total = sum_distance(nums + c * n, ways + c * n, n, ds[c], places);
            sum += total;
            check = (check * 31 + total + r) % 1000000007;
        }
    }
    printf("%d cases of %lld robots, %d rounds: sums mod p sum to %lld, checksum %lld\n", cases, (long long)n, rounds, (long long)sum, (long long)check);
    free(nums); free(ways); free(places);
    return 0;
}
