// LeetCode #2155: All Divisions With the Highest Score of a Binary Array
// -- the benchmark's C mirror of divisions.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2155;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// the divisions go into found, which has room for n + 1; returns how many
static int64_t max_score_indices(const int64_t *nums, int64_t n, int64_t *found) {
    int64_t right_ones = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == 1) {
            right_ones++;
        }
    }
    int64_t left_zeros = 0;
    int64_t top = right_ones;
    int64_t count = 0;
    found[count++] = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == 0) {
            left_zeros++;
        } else {
            right_ones--;
        }
        int64_t score = left_zeros + right_ones;
        if (score > top) {
            top = score;
            count = 0;
        }
        if (score == top) {
            found[count++] = i + 1;
        }
    }
    return count;
}

int main(void) {
    int64_t *lists[4];
    for (int s = 0; s < 4; s++) {
        lists[s] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) {
            lists[s][i] = next_random() % 2;
        }
    }
    int64_t *found = malloc((N + 1) * sizeof(int64_t));
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 50; round++) {
        for (int s = 0; s < 4; s++) {
            int64_t at = next_random() % N;
            lists[s][at] = 1 - lists[s][at];
            int64_t len = max_score_indices(lists[s], N, found);
            total += len;
            check = (check * 31 + len + found[0] + found[len - 1] + round) % 1000000007;
        }
    }
    printf("200 solves: %lld divisions in all, checksum %lld\n", (long long)total, (long long)check);
    for (int s = 0; s < 4; s++) {
        free(lists[s]);
    }
    free(found);
    return 0;
}
