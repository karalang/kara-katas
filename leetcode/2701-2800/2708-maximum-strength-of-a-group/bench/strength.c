// LeetCode #2708: Maximum Strength of a Group -- the bench (strength.kara
// in C): every non-zero number multiplied in, and an odd negative, the
// one nearest zero, divided back out.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_strength(const int64_t *nums, int n) {
    if (n == 1) return nums[0];
    int64_t product = 1, taken = 0, negatives = 0, nearest = -10;
    for (int i = 0; i < n; i++) {
        int64_t v = nums[i];
        if (v != 0) {
            product *= v;
            taken += 1;
        }
        if (v < 0) {
            negatives += 1;
            if (v > nearest) nearest = v;
        }
    }
    if (negatives % 2 == 1) {
        product /= nearest;
        taken -= 1;
    }
    return taken > 0 ? product : 0;
}

static int64_t seed = 2708;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int groups = 1000000, rounds = 10;
    int64_t *nums = malloc(sizeof(int64_t) * groups * 13);
    int *len = malloc(sizeof(int) * groups);
    for (int g = 0; g < groups; g++) {
        len[g] = (int)(next_random() % 13 + 1);
        for (int i = 0; i < len[g]; i++) nums[g * 13 + i] = next_random() % 19 - 9;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int g = 0; g < groups; g++) {
            int64_t strength = max_strength(nums + g * 13, len[g]);
            sum += strength % 1000;
            check = (check * 31 + (strength % 1000000007 + 1000000007) % 1000000007 + r) % 1000000007;
        }
    }
    printf("%d groups of 1 to 13, %d rounds: strengths mod 1000 sum to %lld, checksum %lld\n", groups, rounds, (long long)sum, (long long)check);
    free(nums);
    free(len);
    return 0;
}
