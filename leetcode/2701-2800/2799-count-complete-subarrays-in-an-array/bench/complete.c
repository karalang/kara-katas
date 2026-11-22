// LeetCode #2799: Count Complete Subarrays in an Array -- the bench in C:
// the ★ arm over 2000 arrays of 1000 numbers, half from 1 to 2000 and
// half from 1 to 20, all drawn first, then each answered 20 times. C has
// no map, so the window's counts sit in a table over the numbers, which
// are at most 2000, with the numbers it holds counted beside it.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define COUNT 2000
#define N 1000
#define TOP 2000

static int64_t seed = 2799;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t counts[TOP + 1];
static char seen[TOP + 1];

static int64_t count_complete_subarrays(const int64_t *nums, int64_t n) {
    memset(seen, 0, sizeof seen);
    int64_t d = 0;
    for (int64_t i = 0; i < n; i++)
        if (!seen[nums[i]]) { seen[nums[i]] = 1; d++; }
    memset(counts, 0, sizeof counts);
    int64_t held = 0, start = 0, complete = 0;
    for (int64_t i = 0; i < n; i++) {
        if (counts[nums[i]]++ == 0) held++;
        while (held == d && counts[nums[start]] > 1) {
            counts[nums[start]]--;
            start++;
        }
        if (held == d) complete += start + 1;
    }
    return complete;
}

static int64_t cases[COUNT][N];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++) {
        int64_t top = c % 2 == 0 ? 2000 : 20;
        for (int i = 0; i < N; i++) cases[c][i] = wide() % top + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = count_complete_subarrays(cases[c], N);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d arrays of 1000, %d rounds: complete sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
