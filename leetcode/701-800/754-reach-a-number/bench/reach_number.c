// LeetCode 754 — Reach a Number, bench: the ★ arm (step by step),
// mirrored from reach_number.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t reach_number(int64_t target) {
    int64_t t = target < 0 ? -target : target;
    int64_t k = 0, sum = 0;
    while (sum < t || (sum - t) % 2 != 0) {
        k += 1;
        sum += k;
    }
    return k;
}

static int64_t seed = 754;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rounds = 30000, total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t a = next_random();
        int64_t b = next_random();
        int64_t target = (a * 32768 + b) % 1000000000 + 1;
        if (next_random() % 2 == 0) target = -target;
        int64_t moves = reach_number(target);
        total += moves;
        check = (check * 31 + moves) % 1000000007;
    }
    printf("%lld targets: %lld moves in all, checksum %lld\n", (long long)rounds, (long long)total, (long long)check);
    return 0;
}
