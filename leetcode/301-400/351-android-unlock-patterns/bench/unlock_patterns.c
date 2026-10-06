// Benchmark workload for LeetCode #351 — C mirror of unlock_patterns.kara.
// The same search: a skip table, runs from keys 1, 2 and 5 weighted 4, 4, 1.
// The table and the visited flags are allocated per call, as the Kara arm's
// Vecs are.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ROUNDS 48

static int64_t *skip_table(void) {
    int64_t *skip = calloc(100, sizeof(int64_t));
    static const int64_t pairs[8][3] = {{1, 3, 2}, {4, 6, 5}, {7, 9, 8}, {1, 7, 4},
                                        {2, 8, 5}, {3, 9, 6}, {1, 9, 5}, {3, 7, 5}};
    for (int i = 0; i < 8; i++) {
        skip[pairs[i][0] * 10 + pairs[i][1]] = pairs[i][2];
        skip[pairs[i][1] * 10 + pairs[i][0]] = pairs[i][2];
    }
    return skip;
}

static int64_t count_from(int64_t key, int64_t len, int64_t m, int64_t n, bool *visited,
                          const int64_t *skip) {
    int64_t total = 0;
    if (len >= m) total += 1;
    if (len == n) return total;
    visited[key] = true;
    for (int64_t next = 1; next < 10; next++) {
        int64_t mid = skip[key * 10 + next];
        if (!visited[next] && (mid == 0 || visited[mid])) {
            total += count_from(next, len + 1, m, n, visited, skip);
        }
    }
    visited[key] = false;
    return total;
}

static int64_t number_of_patterns(int64_t m, int64_t n) {
    if (m > n) return 0;
    int64_t *skip = skip_table();
    bool *visited = calloc(10, sizeof(bool));
    int64_t corner = count_from(1, 1, m, n, visited, skip);
    int64_t edge = count_from(2, 1, m, n, visited, skip);
    int64_t center = count_from(5, 1, m, n, visited, skip);
    free(visited);
    free(skip);
    return 4 * corner + 4 * edge + center;
}

int main(void) {
    int64_t sink = 0;
    for (int64_t round = 0; round < ROUNDS; round++) {
        for (int64_t m = 1; m < 10; m++) {
            for (int64_t n = 1; n < 10; n++) {
                int64_t c = number_of_patterns(m, n);
                sink = (sink * 31 + c + round) % 1000000007;
            }
        }
    }
    printf("sink %lld\n", (long long)sink);
    return 0;
}
