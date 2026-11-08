// LeetCode #1504: Count Submatrices With All Ones -- the benchmark, the
// same algorithm as submat.kara: column heights per row and a stack of
// increasing heights.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 150

static int64_t count_submatrices(int64_t (*mat)[SIZE], int64_t m, int64_t n) {
    int64_t *heights = calloc(n, sizeof(int64_t));
    int64_t *ending = malloc(n * sizeof(int64_t));
    int64_t *stack = malloc(n * sizeof(int64_t));
    int64_t total = 0;
    for (int64_t i = 0; i < m; i++) {
        for (int64_t j = 0; j < n; j++) heights[j] = mat[i][j] == 1 ? heights[j] + 1 : 0;
        int64_t top = 0;
        for (int64_t j = 0; j < n; j++) {
            while (top > 0 && heights[stack[top - 1]] >= heights[j]) top--;
            if (top == 0) {
                ending[j] = heights[j] * (j + 1);
            } else {
                int64_t k = stack[top - 1];
                ending[j] = ending[k] + heights[j] * (j - k);
            }
            stack[top++] = j;
            total += ending[j];
        }
    }
    free(heights); free(ending); free(stack);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1504;
    int64_t (*mats)[SIZE][SIZE] = malloc(400 * sizeof(*mats));
    for (int i = 0; i < 400; i++)
        for (int r = 0; r < SIZE; r++)
            for (int c = 0; c < SIZE; c++)
                mats[i][r][c] = next_random(&seed) % 100 < 50 + i % 50 ? 1 : 0;
    int64_t total = 0, check = 0;
    for (int i = 0; i < 400; i++) {
        int64_t answer = count_submatrices(mats[i], SIZE, SIZE);
        total += answer;
        check = mix(check, answer);
    }
    printf("400 matrices of 150 x 150: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(mats);
    return 0;
}
