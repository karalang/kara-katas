// LeetCode #1793: Maximum Score of a Good Subarray -- the bench in C: the ★
// arm over 200 random lists of 1000 numbers built once, 40000 calls.
#include <stdint.h>
#include <stdio.h>

static int32_t maximum_score(const int32_t *nums, int64_t n, int32_t k) {
    int64_t i = k, j = k;
    int32_t low = nums[i], best = low;
    while (i > 0 || j < n - 1) {
        int32_t left = i > 0 ? nums[i - 1] : 0;
        int32_t right = j < n - 1 ? nums[j + 1] : 0;
        if (left > right) {
            i--;
            if (left < low) low = left;
        } else {
            j++;
            if (right < low) low = right;
        }
        int32_t s = low * (int32_t)(j - i + 1);
        if (s > best) best = s;
    }
    return best;
}

static int64_t seed = 1793;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[200][1000];
    for (int l = 0; l < 200; l++)
        for (int x = 0; x < 1000; x++) lists[l][x] = (int32_t)(1 + next_random() % 20000);
    int64_t check = 0;
    for (int64_t call = 0; call < 40000; call++) {
        int64_t k = check % 1000;
        check = (check * 31 + maximum_score(lists[(check + call) % 200], 1000, (int32_t)k)) % 1000000007;
    }
    printf("40000 calls over 200 lists of 1000 numbers: checksum %lld\n", (long long)check);
    return 0;
}
