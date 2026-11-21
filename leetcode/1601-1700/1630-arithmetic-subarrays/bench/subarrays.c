// LeetCode #1630: Arithmetic Subarrays -- the bench's C mirror: the ★ arm
// on 200 random problems of 500 numbers and 500 queries, all drawn first.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { PROBLEMS = 200, N = 500, M = 500 };

static int cmp(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static void check_arithmetic_subarrays(const int32_t *nums, const int32_t *l, const int32_t *r, int m, bool *answers) {
    int32_t *run = malloc(sizeof(int32_t) * N);
    for (int q = 0; q < m; q++) {
        int k = r[q] - l[q] + 1;
        memcpy(run, nums + l[q], sizeof(int32_t) * (size_t)k);
        qsort(run, (size_t)k, sizeof(int32_t), cmp);
        int32_t step = run[1] - run[0];
        bool ok = true;
        for (int i = 1; i < k; i++) {
            if (run[i] - run[i - 1] != step) {
                ok = false;
                break;
            }
        }
        answers[q] = ok;
    }
    free(run);
}

static int64_t seed = 1630;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    static int32_t nums[PROBLEMS][N], l[PROBLEMS][M], r[PROBLEMS][M];
    for (int p = 0; p < PROBLEMS; p++) {
        for (int i = 0; i < N; i++) {
            if (p % 2 == 0) nums[p][i] = 3 * i - 700;
            else nums[p][i] = (int32_t)(wide() % 200001 - 100000);
        }
        for (int i = N - 1; i >= 1; i--) {
            int j = (int)(next_random() % (i + 1));
            int32_t t = nums[p][i];
            nums[p][i] = nums[p][j];
            nums[p][j] = t;
        }
        for (int q = 0; q < M; q++) {
            int64_t a = next_random() % 499;
            l[p][q] = (int32_t)a;
            r[p][q] = (int32_t)(a + 1 + next_random() % (499 - a));
        }
    }
    int64_t check = 0, yes = 0;
    static bool answers[M];
    for (int p = 0; p < PROBLEMS; p++) {
        check_arithmetic_subarrays(nums[p], l[p], r[p], M, answers);
        for (int q = 0; q < M; q++) {
            if (answers[q]) yes++;
            check = (check * 31 + answers[q] + 1) % 1000000007;
        }
    }
    printf("200 problems of 500 numbers and 500 queries: %lld arithmetic, checksum %lld\n", (long long)yes, (long long)check);
    return 0;
}
