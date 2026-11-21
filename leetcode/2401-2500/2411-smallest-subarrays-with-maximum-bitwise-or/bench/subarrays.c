// LeetCode #2411: Smallest Subarrays With Maximum Bitwise OR -- the bench,
// the ★ arm in C: walking from the right, the nearest index holding each
// of the 30 bits, the subarray from i reaching the farthest of them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2411;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t *smallest_subarrays(const int64_t *nums, int64_t n) {
    int64_t nearest[30];
    for (int b = 0; b < 30; b++) nearest[b] = -1;
    int64_t *answer = malloc(n * sizeof *answer);
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t reach = i;
        for (int bit = 0; bit < 30; bit++) {
            if (nums[i] >> bit & 1) nearest[bit] = i;
            if (nearest[bit] > reach) reach = nearest[bit];
        }
        answer[i] = reach - i + 1;
    }
    return answer;
}

int main(void) {
    static int64_t arrays[5][N];
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < N; j++) arrays[i][j] = (next_random() * 32768 + next_random()) % ((int64_t)1 << (6 * i + 6));
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int i = 0; i < 5; i++) {
            int64_t *answer = smallest_subarrays(arrays[i], N);
            for (int j = 0; j < N; j++) check = (check * 31 + answer[j] + p) % 1000000007;
            free(answer);
        }
    printf("10 passes over 5 arrays of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
