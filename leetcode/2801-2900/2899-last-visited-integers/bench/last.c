// LeetCode #2899: Last Visited Integers -- the bench's C mirror (last.kara): seen
// and the answers in buffers allocated per call, as the other languages'
// vectors are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *last_visited_integers(const int64_t *nums, int64_t n, int64_t *len) {
    int64_t *seen = malloc(sizeof(int64_t) * n);
    int64_t *ans = malloc(sizeof(int64_t) * n);
    int64_t s = 0, a = 0, k = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == -1) {
            k++;
            ans[a++] = k <= s ? seen[s - k] : -1;
        } else {
            seen[s++] = nums[i];
            k = 0;
        }
    }
    free(seen);
    *len = a;
    return ans;
}

static int64_t seed = 2899;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 10000, ROUNDS = 20, N = 100 };
    static int64_t cases[COUNT][N];
    for (int c = 0; c < COUNT; c++)
        for (int i = 0; i < N; i++)
            cases[c][i] = next_random() % 3 == 0 ? -1 : next_random() % 100 + 1;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            int64_t len;
            int64_t *ans = last_visited_integers(cases[c], N, &len);
            check = (check * 31 + len + r) % 1000000007;
            for (int64_t i = 0; i < len; i++) {
                total += ans[i];
                check = (check * 31 + ans[i] + 2) % 1000000007;
            }
            free(ans);
        }
    printf("%d arrays of %d, %d rounds: answers total %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)check);
    return 0;
}
