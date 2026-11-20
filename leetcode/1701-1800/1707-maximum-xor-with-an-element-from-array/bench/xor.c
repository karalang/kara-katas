// LeetCode #1707: Maximum XOR With an Element From Array -- the bench's C
// mirror: the ★ arm on 4 random problems of 100000 values and 100000
// queries, all drawn first, each answered 3 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 4
#define ROUNDS 3
#define N 100000

static int cmp_i32(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static const int32_t (*sort_queries)[2];

static int cmp_by_limit(const void *a, const void *b) {
    int32_t x = sort_queries[*(const int64_t *)a][1], y = sort_queries[*(const int64_t *)b][1];
    return (x > y) - (x < y);
}

// the queries offline by limit, against a 30-bit trie of the values allowed
static void maximize_xor(const int32_t *nums, int64_t n, const int32_t (*queries)[2], int64_t q, int32_t *answer) {
    int32_t *values = malloc((size_t)n * sizeof *values);
    for (int64_t i = 0; i < n; i++) {
        values[i] = nums[i];
    }
    qsort(values, (size_t)n, sizeof *values, cmp_i32);
    int64_t *order = malloc((size_t)q * sizeof *order);
    for (int64_t i = 0; i < q; i++) {
        order[i] = i;
    }
    sort_queries = queries;
    qsort(order, (size_t)q, sizeof *order, cmp_by_limit);
    // children of each node, 0 for none: the root is node 0
    int64_t (*trie)[2] = malloc(((size_t)n * 30 + 1) * sizeof *trie);
    int64_t nodes = 1;
    trie[0][0] = trie[0][1] = 0;
    int64_t next = 0;
    for (int64_t k = 0; k < q; k++) {
        int64_t i = order[k];
        int64_t x = queries[i][0], m = queries[i][1];
        while (next < n && values[next] <= m) {
            int64_t node = 0;
            for (int bit = 29; bit >= 0; bit--) {
                int64_t b = values[next] >> bit & 1;
                if (trie[node][b] == 0) {
                    trie[nodes][0] = trie[nodes][1] = 0;
                    trie[node][b] = nodes++;
                }
                node = trie[node][b];
            }
            next++;
        }
        if (next == 0) {
            answer[i] = -1;
            continue;
        }
        int64_t node = 0, best = 0;
        for (int bit = 29; bit >= 0; bit--) {
            int64_t want = (x >> bit & 1) ^ 1;
            if (trie[node][want] != 0) {
                best |= (int64_t)1 << bit;
                node = trie[node][want];
            } else {
                node = trie[node][want ^ 1];
            }
        }
        answer[i] = (int32_t)best;
    }
    free(trie);
    free(order);
    free(values);
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1707;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// a random value below 10^9, from two draws
static int64_t value(void) {
    int64_t a = next_random();
    return (a * 32768 + next_random()) % 1000000000;
}

int main(void) {
    int32_t *nums = malloc((size_t)COUNT * N * sizeof *nums);
    int32_t (*queries)[2] = malloc((size_t)COUNT * N * sizeof *queries);
    for (int c = 0; c < COUNT; c++) {
        for (int64_t i = 0; i < N; i++) {
            nums[(int64_t)c * N + i] = (int32_t)value();
        }
        for (int64_t i = 0; i < N; i++) {
            int32_t x = (int32_t)value();
            queries[(int64_t)c * N + i][0] = x;
            queries[(int64_t)c * N + i][1] = (int32_t)value();
        }
    }
    int32_t *answer = malloc(N * sizeof *answer);
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            maximize_xor(nums + (int64_t)c * N, N, (const int32_t (*)[2])(queries + (int64_t)c * N), N, answer);
            for (int64_t i = 0; i < N; i++) {
                sum += answer[i];
                check = (check * 31 + answer[i] + 1 + r) % 1000000007;
            }
        }
    }
    printf("%d problems of %d values and %d queries, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, N, ROUNDS, (long long)sum, (long long)check);
    free(answer);
    free(queries);
    free(nums);
    return 0;
}
