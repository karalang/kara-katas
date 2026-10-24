// LeetCode #991: Broken Calculator -- bench, the ★ arm (greedy from the
// target back), the same algorithm and workload as broken_calc.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t broken_calc(int64_t start_value, int64_t target) {
    int64_t ops = 0, t = target;
    while (t > start_value) {
        if (t % 2 == 1) t += 1;
        else t /= 2;
        ops += 1;
    }
    return ops + start_value - t;
}

static int64_t seed = 991;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 5000;
    int64_t starts[1000], targets[1000];
    for (int i = 0; i < 1000; i++) {
        int64_t a = next_random();
        starts[i] = 1 + (a * 32768 + next_random()) % 1000;
        int64_t b = next_random();
        targets[i] = 1 + (b * 32768 + next_random()) % 1000000000;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 1000; i++) {
            int64_t got = broken_calc(starts[(r + i) % 1000], targets[i]);
            total += got;
            check = (check * 31 + got + 1) % 1000000007;
        }
    }
    printf("%d rounds over 1000 pairs: %lld operations, checksum %lld\n", rounds, (long long)total,
           (long long)check);
    return 0;
}
