// LeetCode #868: Binary Gap -- C mirror of the bench program (the ★ arm,
// one pass over the bits).
#include <stdint.h>
#include <stdio.h>

static int64_t binary_gap(int64_t n) {
    int64_t best = 0;
    int64_t last = -1;
    int64_t rest = n;
    int64_t position = 0;
    while (rest > 0) {
        if (rest % 2 == 1) {
            if (last >= 0 && position - last > best) best = position - last;
            last = position;
        }
        rest /= 2;
        position++;
    }
    return best;
}

int main(void) {
    int64_t limit = 10000000;
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t n = 1; n <= limit; n++) {
        int64_t g = binary_gap(n);
        total += g;
        check = (check * 31 + g) % 1000000007;
    }
    printf("n from 1 to %lld: gaps sum to %lld, checksum %lld\n", (long long)limit, (long long)total,
           (long long)check);
    return 0;
}
