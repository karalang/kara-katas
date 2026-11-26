// LeetCode #1770: Maximum Score from Performing Multiplication Operations
// -- the bench in C, mirroring maximum_score.kara: one row of the table,
// filled from the last operation back to the first, a new row each call.
#include <stdio.h>
#include <stdlib.h>

static int maximum_score(const int *nums, int n, const int *multipliers, int m) {
    int *best = calloc(m + 1, sizeof(int));
    for (int i = m - 1; i >= 0; i--) {
        for (int left = 0; left <= i; left++) {
            int right = n - 1 - (i - left);
            int take_left = multipliers[i] * nums[left] + best[left + 1];
            int take_right = multipliers[i] * nums[right] + best[left];
            best[left] = take_left > take_right ? take_left : take_right;
        }
    }
    int answer = best[0];
    free(best);
    return answer;
}

static long long seed = 1770;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int numbers[100][1000], weights[100][300];
    for (int r = 0; r < 100; r++)
        for (int i = 0; i < 1000; i++) numbers[r][i] = (int)(next_random() % 2001 - 1000);
    for (int r = 0; r < 100; r++)
        for (int i = 0; i < 300; i++) weights[r][i] = (int)(next_random() % 2001 - 1000);
    long long check = 0;
    for (long long call = 0; call < 2000; call++) {
        int score = maximum_score(numbers[(check + call * 7919) % 100], 1000, weights[(check / 100 + call) % 100], 300);
        check = (check * 31 + score % 1000000007LL + 1000000007LL) % 1000000007LL;
    }
    printf("2000 calls over 100 lists: checksum %lld\n", check);
    return 0;
}
