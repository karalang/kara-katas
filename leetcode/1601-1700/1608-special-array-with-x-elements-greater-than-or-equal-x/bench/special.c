// LeetCode #1608: Special Array With X Elements Greater Than or Equal X --
// the bench in C, mirroring special.kara: a copy of the numbers sorted
// largest first with qsort, `x` special when the `x`th largest is at
// least `x` and the next is below it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PROBLEMS 1000
#define N 10000

static int descending(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (y > x) - (y < x);
}

static int special_array(const int *src, int n, int *nums) {
    memcpy(nums, src, n * sizeof(int));
    qsort(nums, n, sizeof(int), descending);
    for (int x = 1; x <= n; x++)
        if (nums[x - 1] >= x && (x == n || nums[x] < x)) return x;
    return -1;
}

static int64_t seed = 1608;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int *problems = malloc(sizeof(int) * PROBLEMS * N);
    for (int i = 0; i < PROBLEMS * N; i++) {
        int64_t a = next_random();
        int64_t b = next_random();
        problems[i] = (int)((a * 32768 + b) % 10001);
    }
    int *scratch = malloc(sizeof(int) * N);
    int64_t check = 0, special = 0;
    for (int p = 0; p < PROBLEMS; p++) {
        int x = special_array(problems + p * N, N, scratch);
        if (x >= 0) special++;
        check = (check * 31 + x + 1) % 1000000007;
    }
    printf("1000 problems of 10000 numbers from 0 to 10000: %lld special, checksum %lld\n",
           (long long)special, (long long)check);
    free(scratch); free(problems);
    return 0;
}
