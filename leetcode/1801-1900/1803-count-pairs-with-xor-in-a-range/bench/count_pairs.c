// LeetCode #1803: Count Pairs With XOR in a Range -- the bench in C: the ★
// arm over 40 random lists of 20000 numbers built once, 100 calls.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BITS 15
#define NODES (20000 * BITS + 1)

static int64_t children[2 * NODES];
static int64_t counts[NODES];

static int64_t count_below(const int32_t *nums, int n, int32_t limit) {
    int64_t len = 1;
    children[0] = children[1] = 0;
    counts[0] = 0;
    int64_t pairs = 0;
    for (int i = 0; i < n; i++) {
        int32_t x = nums[i];
        int64_t node = 0;
        for (int b = BITS - 1; b >= 0; b--) {
            int64_t xb = x >> b & 1;
            if (limit >> b & 1) {
                int64_t same = children[2 * node + xb];
                if (same != 0) pairs += counts[same];
                node = children[2 * node + 1 - xb];
            } else {
                node = children[2 * node + xb];
            }
            if (node == 0) break;
        }
        int64_t at = 0;
        counts[0] += 1;
        for (int b = BITS - 1; b >= 0; b--) {
            int64_t xb = x >> b & 1;
            if (children[2 * at + xb] == 0) {
                children[2 * at + xb] = len;
                counts[len] = 0;
                children[2 * len] = children[2 * len + 1] = 0;
                len++;
            }
            at = children[2 * at + xb];
            counts[at] += 1;
        }
    }
    return pairs;
}

static int32_t count_pairs(const int32_t *nums, int n, int32_t low, int32_t high) {
    return (int32_t)(count_below(nums, n, high + 1) - count_below(nums, n, low));
}

static int64_t seed = 1803;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t lists[40][20000];
    for (int l = 0; l < 40; l++)
        for (int x = 0; x < 20000; x++) lists[l][x] = (int32_t)(1 + next_random() % 20000);
    int64_t check = 0;
    for (int64_t call = 0; call < 100; call++) {
        int64_t low = 1 + next_random() % 20000;
        int64_t high = low + next_random() % (20001 - low);
        check = (check * 31 + count_pairs(lists[(check + call) % 40], 20000, (int32_t)low, (int32_t)high)) % 1000000007;
    }
    printf("100 calls over 40 lists of 20000 numbers: checksum %lld\n", (long long)check);
    return 0;
}
