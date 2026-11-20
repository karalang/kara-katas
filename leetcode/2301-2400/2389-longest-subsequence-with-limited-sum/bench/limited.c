// LeetCode #2389: Longest Subsequence With Limited Sum -- the bench, the
// ★ arm in C: the values sorted into prefix sums, each query answered by
// binary search.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// The answers go into a fresh allocation, as the other languages' Vec
// does; the caller frees it.
static int64_t *answer_queries(const int64_t *nums, int64_t n, const int64_t *queries, int64_t m) {
    int64_t *prefix = malloc(sizeof(int64_t) * n);
    memcpy(prefix, nums, sizeof(int64_t) * n);
    qsort(prefix, n, sizeof(int64_t), cmp);
    for (int64_t i = 1; i < n; i++) prefix[i] += prefix[i - 1];
    int64_t *answer = malloc(sizeof(int64_t) * m);
    for (int64_t j = 0; j < m; j++) {
        int64_t low = 0, high = n;
        while (low < high) {
            int64_t mid = (low + high) / 2;
            if (prefix[mid] <= queries[j]) low = mid + 1;
            else high = mid;
        }
        answer[j] = low;
    }
    free(prefix);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t high = next_random(seed);
    return high * 32768 + next_random(seed);
}

static int64_t arrays[100][1000];
static int64_t asks[100][1000];

int main(void) {
    // 100 arrays of 1000 values up to 10^6, each with 1000 queries up to
    // 10^9; each pass answers them all and folds every answer
    int64_t seed = 2389;
    for (int a = 0; a < 100; a++) {
        for (int i = 0; i < 1000; i++) arrays[a][i] = 1 + wide(&seed) % 1000000;
        for (int i = 0; i < 1000; i++) asks[a][i] = 1 + wide(&seed) % 1000000000;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++) {
        for (int a = 0; a < 100; a++) {
            int64_t *answer = answer_queries(arrays[a], 1000, asks[a], 1000);
            for (int j = 0; j < 1000; j++) check = (check * 31 + answer[j] + p) % 1000000007;
            free(answer);
        }
    }
    printf("200 passes over 100 arrays of 1000 values and 1000 queries: checksum %lld\n", (long long)check);
    return 0;
}
