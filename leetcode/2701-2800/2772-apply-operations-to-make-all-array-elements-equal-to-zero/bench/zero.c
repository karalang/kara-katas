// LeetCode #2772: Apply Operations to Make All Array Elements Equal to
// Zero -- the bench in C: the ★ arm over 20 arrays of 10^5 numbers, all
// drawn first, then each answered 40 times.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define COUNT 20
#define N 100000

static int64_t seed = 2772;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t ends[N + 1];

static int check_array(const int64_t *nums, int64_t n, int64_t k) {
    memset(ends, 0, sizeof(int64_t) * (n + 1));
    int64_t covering = 0;
    for (int64_t i = 0; i < n; i++) {
        covering -= ends[i];
        int64_t left = nums[i] - covering;
        if (left < 0) return 0;
        if (left > 0) {
            if (i + k > n) return 0;
            covering += left;
            ends[i + k] += left;
        }
    }
    return 1;
}

static int64_t ops[N];

static void built(int64_t *nums, int64_t n, int64_t k, int64_t most) {
    int64_t running = 0;
    for (int64_t i = 0; i < n; i++) {
        ops[i] = 0;
        if (i + k <= n) ops[i] = next_random() % (most + 1);
        running += ops[i];
        if (i >= k) running -= ops[i - k];
        nums[i] = running;
    }
    if (next_random() % 2 == 1) {
        int64_t at = wide() % n;
        if (nums[at] > 0 && next_random() % 2 == 1) {
            nums[at] -= 1;
        } else {
            nums[at] += 1;
        }
    }
}

static int64_t cases[COUNT][N], ks[COUNT];

int main(void) {
    int rounds = 40;
    for (int c = 0; c < COUNT; c++) {
        ks[c] = wide() % 1000 + 1;
        built(cases[c], N, ks[c], 9);
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int a = check_array(cases[c], N, ks[c]);
            yes += a;
            check = (check * 31 + (a ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%d arrays of 10^5, %d rounds: %lld true, checksum %lld\n", COUNT, rounds, (long long)yes, (long long)check);
    return 0;
}
