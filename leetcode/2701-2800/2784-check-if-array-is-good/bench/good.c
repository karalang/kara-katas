// LeetCode #2784: Check if Array is Good -- the bench in C: the ★ arm
// over 50000 arrays of 100 numbers, base[99] shuffled and two in three
// with one number changed to one up to 200, all drawn first, then each
// answered 40 times.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define COUNT 50000
#define LEN 100

static int64_t seed = 2784;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int is_good(const int64_t *nums, int64_t len) {
    int64_t n = len - 1;
    if (n < 1) return 0;
    int64_t counts[LEN];
    memset(counts, 0, sizeof(int64_t) * (n + 1));
    for (int64_t i = 0; i < len; i++) {
        int64_t v = nums[i];
        if (v < 1 || v > n) return 0;
        counts[v]++;
    }
    for (int64_t v = 1; v < n; v++)
        if (counts[v] != 1) return 0;
    return counts[n] == 2;
}

static int64_t cases[COUNT][LEN];

int main(void) {
    int rounds = 40;
    for (int c = 0; c < COUNT; c++) {
        int64_t *nums = cases[c];
        for (int64_t i = 0; i < 99; i++) nums[i] = i + 1;
        nums[99] = 99;
        for (int64_t i = 99; i > 0; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
        if (next_random() % 3 != 0) {
            int64_t at = next_random() % 100;
            nums[at] = next_random() % 200 + 1;
        }
    }
    int64_t good = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int g = is_good(cases[c], LEN);
            good += g;
            check = (check * 31 + (g ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%d arrays of 100, %d rounds: %lld good, checksum %lld\n", COUNT, rounds, (long long)good, (long long)check);
    return 0;
}
