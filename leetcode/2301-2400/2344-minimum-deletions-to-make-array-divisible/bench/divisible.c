// LeetCode #2344: Minimum Deletions to Make Array Divisible -- the bench,
// the ★ arm in C: the gcd of numsDivide, then nums sorted and scanned for
// the first value that divides it.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t gcd(int64_t a, int64_t b) {
    while (b != 0) {
        int64_t t = a % b;
        a = b;
        b = t;
    }
    return a;
}

static int cmp(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t min_operations(const int64_t *nums, int64_t n, const int64_t *nums_divide, int64_t m) {
    int64_t g = 0;
    for (int64_t i = 0; i < m; i++) g = gcd(g, nums_divide[i]);
    int64_t *sorted = malloc(n * sizeof(int64_t));
    memcpy(sorted, nums, n * sizeof(int64_t));
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t answer = -1;
    for (int64_t i = 0; i < n; i++) {
        if (g % sorted[i] == 0) {
            answer = i;
            break;
        }
    }
    free(sorted);
    return answer;
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    int64_t *nums[10], *divide[10];
    for (int64_t a = 0; a < 10; a++) {
        nums[a] = malloc(100000 * sizeof(int64_t));
        divide[a] = malloc(10000 * sizeof(int64_t));
        for (int64_t i = 0; i < 100000; i++) nums[a][i] = scrambled(a * 100000 + i) % 1000000 + 1;
        int64_t base = nums[a][a * 7919 % 100000];
        for (int64_t i = 0; i < 10000; i++) divide[a][i] = base * (scrambled(a * 10000 + i + 7) % 1000 + 1);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++)
        for (int a = 0; a < 10; a++)
            check = (check * 31 + min_operations(nums[a], 100000, divide[a], 10000) + p) % 1000000007;
    printf("20 passes over 10 cases of 10^5 values against 10^4: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(nums[a]);
        free(divide[a]);
    }
    return 0;
}
