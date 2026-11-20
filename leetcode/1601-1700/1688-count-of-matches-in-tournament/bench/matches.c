// LeetCode #1688: Count of Matches in Tournament -- the bench's C mirror:
// the ★ arm on 500000 random n up to 10^9, all drawn first, each answered
// 40 times.

#include <stdint.h>
#include <stdio.h>

#define COUNT 500000
#define ROUNDS 40

static int32_t matches(int32_t n) {
    int32_t teams = n, played = 0;
    while (teams > 1) {
        played += teams / 2;
        teams = (teams + 1) / 2;
    }
    return played;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1688;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t values[COUNT];
    for (int i = 0; i < COUNT; i++) {
        int64_t hi = next_random();
        values[i] = (int32_t)((hi * 32768 + next_random()) % 1000000000 + 1);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int i = 0; i < COUNT; i++) {
            int32_t answer = matches(values[i]);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d values of n, %d rounds: %lld matches, checksum %lld\n", COUNT, ROUNDS, (long long)total, (long long)check);
    return 0;
}
