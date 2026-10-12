// Benchmark for #398: mirror of random_pick_index.kara (reservoir sampling).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *nums;
    int64_t n;
    int64_t seed;
} Solution;

static int64_t below(Solution *s, int64_t n) {
    s->seed = (s->seed * 1103515245 + 12345) % 2147483648;
    return (s->seed / 65536) % n;
}

static int64_t pick(Solution *s, int64_t target) {
    int64_t kept = -1, seen = 0;
    for (int64_t i = 0; i < s->n; i++) {
        if (s->nums[i] == target) {
            seen += 1;
            if (below(s, seen) == 0) {
                kept = i;
            }
        }
    }
    return kept;
}

int main(int argc, char **argv) {
    int64_t picks = argc > 1 ? atoll(argv[1]) : 10000;
    int64_t seed = 3980;
    int64_t *nums = malloc(20000 * sizeof(int64_t));
    for (int i = 0; i < 20000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        nums[i] = (seed / 65536) % 10;
    }
    Solution s = {nums, 20000, 398};
    int64_t total = 0, checksum = 0;
    for (int64_t p = 0; p < picks; p++) {
        int64_t r = pick(&s, p % 10);
        total += r;
        checksum = (checksum * 31 + r) % 1000000007;
    }
    printf("%lld picks: total %lld, checksum %lld\n", (long long)picks, (long long)total, (long long)checksum);
    free(nums);
    return 0;
}
