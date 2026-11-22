// LeetCode #2780: Minimum Index of a Valid Split -- the bench in C: the
// ★ arm over 20 arrays of 10^5 numbers up to 10^9, each with a dominant
// number, all drawn first, then each answered 100 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 20
#define N 100000

static int64_t seed = 2780;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t minimum_index(const int64_t *nums, int64_t n) {
    int64_t x = 0, votes = 0;
    for (int64_t i = 0; i < n; i++) {
        if (votes == 0) x = nums[i];
        votes += nums[i] == x ? 1 : -1;
    }
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i] == x;
    int64_t left = 0;
    for (int64_t i = 0; i < n - 1; i++) {
        if (nums[i] == x) left++;
        if (2 * left > i + 1 && 2 * (total - left) > n - i - 1) return i;
    }
    return -1;
}

static int64_t cases[COUNT][N];

static void dominated(int64_t *nums, int64_t n, int64_t others, int64_t top) {
    int64_t x = wide() % top + 1;
    int64_t many = n / 2 + 1 + wide() % (n - n / 2);
    int64_t len = 0;
    while (len < many) nums[len++] = x;
    while (len < n) {
        int64_t v = wide() % others + 1;
        if (v != x) nums[len++] = v;
    }
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = wide() % (i + 1);
        int64_t t = nums[i];
        nums[i] = nums[j];
        nums[j] = t;
    }
}

int main(void) {
    int rounds = 100;
    for (int c = 0; c < COUNT; c++) dominated(cases[c], N, 1000000000, 1000000000);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = minimum_index(cases[c], N);
            total += a;
            check = (check * 31 + a + 1 + r) % 1000000007;
        }
    }
    printf("%d arrays of 10^5, %d rounds: indices sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
