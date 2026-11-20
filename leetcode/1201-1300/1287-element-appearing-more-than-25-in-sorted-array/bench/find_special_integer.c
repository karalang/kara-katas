// LeetCode #1287 bench, in C: the ★ arm (the first i where arr[i] equals
// arr[i + n / 4]) on 100 sorted arrays of 10^5 numbers, built once, 1000
// rounds, every answer folded into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_special_integer(const int64_t *arr, int64_t n) {
    int64_t quarter = n / 4;
    for (int64_t i = 0; i < n - quarter; i++)
        if (arr[i] == arr[i + quarter]) return arr[i];
    return -1;
}

static int64_t seed;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t *problem(int64_t n) {
    int64_t planted = next_random() % 100001;
    int64_t times = n / 4 + 1 + next_random() % (n / 4);
    int64_t *arr = malloc(n * sizeof(int64_t)), len = 0;
    while (len < times) arr[len++] = planted;
    while (len < n) {
        int64_t x = next_random() % 100001;
        if (x != planted) arr[len++] = x;
    }
    qsort(arr, n, sizeof(int64_t), cmp);
    return arr;
}

int main(void) {
    seed = 1287;
    int64_t *problems[100];
    for (int k = 0; k < 100; k++) problems[k] = problem(100000);
    int64_t check = 0;
    for (int64_t round = 0; round < 1000; round++)
        for (int k = 0; k < 100; k++)
            check = (check * 131 + find_special_integer(problems[k], 100000) + round) % 1000000007;
    printf("1000 rounds of 100 arrays of 100000 numbers: checksum %lld\n", (long long)check);
    return 0;
}
