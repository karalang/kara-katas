// LeetCode #2769: Find the Maximum Achievable Number -- the bench in C:
// the ★ arm over 10^6 random pairs, all drawn first, then each answered
// 50 times into a running checksum.
#include <stdint.h>
#include <stdio.h>

#define COUNT 1000000

static int64_t seed = 2769;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t the_maximum_achievable_x(int64_t num, int64_t t) { return num + 2 * t; }

static int64_t nums[COUNT], ts[COUNT];

int main(void) {
    int rounds = 50;
    for (int i = 0; i < COUNT; i++) {
        nums[i] = next_random() % 50 + 1;
        ts[i] = next_random() % 50 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            int64_t x = the_maximum_achievable_x(nums[i], ts[i]);
            total += x;
            check = (check * 31 + x + r) % 1000000007;
        }
    }
    printf("%d pairs, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
