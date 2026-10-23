// LeetCode #932: Beautiful Array -- bench: divide and conquer with a
// memo. Mirrors beautiful_array.kara, .rs, .py and go-seq/. The memo is
// an array indexed by n, each size's array kept as its own copy.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *items[1002];
} Memo;

static int64_t *copy_of(const int64_t *src, int64_t len) {
    int64_t *dst = malloc(sizeof(int64_t) * (size_t)len);
    memcpy(dst, src, sizeof(int64_t) * (size_t)len);
    return dst;
}

// returns a new array of n values, the caller frees it
static int64_t *build(int64_t n, Memo *memo) {
    if (memo->items[n] != NULL) {
        return copy_of(memo->items[n], n);
    }
    int64_t *out = malloc(sizeof(int64_t) * (size_t)n);
    if (n == 1) {
        out[0] = 1;
    } else {
        int64_t odd = (n + 1) / 2;
        int64_t even = n / 2;
        int64_t *a = build(odd, memo);
        for (int64_t i = 0; i < odd; i++) {
            out[i] = 2 * a[i] - 1;
        }
        free(a);
        int64_t *b = build(even, memo);
        for (int64_t i = 0; i < even; i++) {
            out[odd + i] = 2 * b[i];
        }
        free(b);
    }
    memo->items[n] = copy_of(out, n);
    return out;
}

static int64_t *beautiful_array(int64_t n) {
    Memo memo;
    memset(&memo, 0, sizeof(memo));
    int64_t *nums = build(n, &memo);
    for (int64_t k = 0; k <= n; k++) {
        free(memo.items[k]);
    }
    return nums;
}

int main(void) {
    int64_t rounds = 100;
    int64_t top = 1000;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round builds the array for every n from 1 to top, starting
        // from a different n
        for (int64_t i = 0; i < top; i++) {
            int64_t n = (r + i) % top + 1;
            int64_t *nums = beautiful_array(n);
            total += nums[n / 2];
            check = (check * 1000003 + nums[n - 1]) % 1000000007;
            free(nums);
        }
    }
    printf("%lld rounds over n from 1 to %lld: middles summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)top, (long long)total, (long long)check);
    return 0;
}
