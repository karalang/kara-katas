// LeetCode #2831: Find the Longest Equal Subarray -- the bench, mirrored
// from equal.kara: positions per value, then two pointers over each list.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

// Each value's positions, laid out by a counting pass: start[v] .. start[v + 1].
static int64_t longest_equal_subarray(const int64_t *nums, int64_t n, int64_t k,
                                      int64_t *start, int64_t *fill, int64_t *pos) {
    for (int64_t v = 0; v <= n + 1; v++) start[v] = 0;
    for (int64_t i = 0; i < n; i++) start[nums[i] + 1]++;
    for (int64_t v = 0; v <= n; v++) start[v + 1] += start[v];
    for (int64_t v = 0; v <= n; v++) fill[v] = start[v];
    for (int64_t i = 0; i < n; i++) pos[fill[nums[i]]++] = i;
    int64_t best = 0;
    for (int64_t v = 0; v <= n; v++) {
        const int64_t *p = pos + start[v];
        int64_t len = start[v + 1] - start[v];
        int64_t l = 0;
        for (int64_t r = 0; r < len; r++) {
            while (p[r] - p[l] - (r - l) > k) l++;
            if (r - l + 1 > best) best = r - l + 1;
        }
    }
    return best;
}

int main(void) {
    const int64_t count = 20, rounds = 20, n = 100000;
    int64_t seed = 2831;
    int64_t *nums = malloc(sizeof(int64_t) * count * n);
    int64_t ks[20];
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) nums[c * n + i] = next_random(&seed) % 1000 + 1;
        ks[c] = next_random(&seed) % 1001;
    }
    int64_t *start = malloc(sizeof(int64_t) * (n + 2));
    int64_t *fill = malloc(sizeof(int64_t) * (n + 1));
    int64_t *pos = malloc(sizeof(int64_t) * n);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t a = longest_equal_subarray(nums + c * n, n, ks[c], start, fill, pos);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: lengths total %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(nums); free(start); free(fill); free(pos);
    return 0;
}
