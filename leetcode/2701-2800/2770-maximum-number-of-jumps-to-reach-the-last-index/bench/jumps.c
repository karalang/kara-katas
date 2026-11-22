// LeetCode #2770: Maximum Number of Jumps to Reach the Last Index -- the
// bench in C: the ★ arm over 40 arrays of 1000 numbers, all drawn first,
// then each answered 5 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 40
#define N 1000

static int64_t seed = 2770;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    int64_t b = next_random();
    return (a * 32768 + b) * 32768 + next_random();
}

static int64_t maximum_jumps(const int64_t *nums, int64_t n, int64_t target) {
    int64_t most[N];
    for (int64_t i = 0; i < n; i++) most[i] = -1;
    most[0] = 0;
    for (int64_t j = 1; j < n; j++) {
        for (int64_t i = 0; i < j; i++) {
            int64_t d = nums[j] - nums[i];
            if (d < 0) d = -d;
            if (most[i] >= 0 && d <= target && most[i] + 1 > most[j]) {
                most[j] = most[i] + 1;
            }
        }
    }
    return most[n - 1];
}

static int64_t nums[COUNT][N], targets[COUNT];

int main(void) {
    int rounds = 5;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) nums[c][i] = wide() % 2000000001 - 1000000000;
        targets[c] = wide() % 2000000001;
    }
    int64_t reached = 0, total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = maximum_jumps(nums[c], N, targets[c]);
            if (a >= 0) {
                reached += 1;
                total += a;
            }
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    printf("%d arrays of 1000, %d rounds: %lld reached, jumps sum to %lld, checksum %lld\n", COUNT, rounds, (long long)reached, (long long)total, (long long)check);
    return 0;
}
