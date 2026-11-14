// LeetCode #1569: Number of Ways to Reorder Array to Get Same BST -- bench:
// the ★ arm (the interleavings, by recursion and Pascal's triangle) over 20
// permutations of 1 to 1000, built once; 15 passes, each first swapping two
// values of every permutation.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t ways(const int64_t *nums, int64_t n, int64_t **choose) {
    if (n <= 2) return 1;
    int64_t root = nums[0];
    int64_t *left = malloc(sizeof(int64_t) * n), *right = malloc(sizeof(int64_t) * n);
    int64_t l = 0, r = 0;
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] < root) left[l++] = nums[i];
        else if (nums[i] > root) right[r++] = nums[i];
    }
    int64_t result = choose[n - 1][l] * ways(left, l, choose) % MOD * ways(right, r, choose) % MOD;
    free(left);
    free(right);
    return result;
}

static int64_t num_of_ways(const int64_t *nums, int64_t n) {
    int64_t **choose = malloc(sizeof(int64_t *) * (n + 1));
    for (int64_t i = 0; i <= n; i++) choose[i] = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 0; i <= n; i++) {
        choose[i][0] = 1;
        for (int64_t j = 1; j <= i; j++) choose[i][j] = (choose[i - 1][j - 1] + choose[i - 1][j]) % MOD;
    }
    int64_t result = (ways(nums, n, choose) - 1 + MOD) % MOD;
    for (int64_t i = 0; i <= n; i++) free(choose[i]);
    free(choose);
    return result;
}

static int64_t seed = 1569;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t n = 1000;
    static int64_t perms[20][1000];
    for (int p = 0; p < 20; p++) {
        for (int64_t i = 0; i < n; i++) perms[p][i] = i + 1;
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t a = next_random();
            int64_t j = (a * 32768 + next_random()) % (i + 1);
            int64_t t = perms[p][i];
            perms[p][i] = perms[p][j];
            perms[p][j] = t;
        }
    }
    int64_t check = 0, total = 0;
    for (int64_t pass = 0; pass < 15; pass++) {
        for (int64_t p = 0; p < 20; p++) {
            int64_t i = (pass * 7919 + p * 104729) % n, j = (pass * 104729 + p * 7919 + 1) % n;
            int64_t t = perms[p][i];
            perms[p][i] = perms[p][j];
            perms[p][j] = t;
            int64_t w = num_of_ways(perms[p], n);
            total = (total + w) % MOD;
            check = mix(check, w);
        }
    }
    printf("15 passes over 20 permutations of 1000 values: ways sum %lld, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
