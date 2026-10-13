// Benchmark for #526: C mirror of the ★ arm (place positions from the
// front); see count_arrangement.kara. A fresh `used` array for every n,
// as the ★ arm's `vec![false; n + 1]`.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t place(int64_t n, int64_t pos, bool *used) {
    if (pos > n) return 1;
    int64_t count = 0;
    for (int64_t x = 1; x <= n; x++) {
        if (!used[x] && (x % pos == 0 || pos % x == 0)) {
            used[x] = true;
            count += place(n, pos + 1, used);
            used[x] = false;
        }
    }
    return count;
}

static int64_t count_arrangement(int64_t n) {
    bool *used = calloc(n + 1, sizeof(bool));
    int64_t count = place(n, 1, used);
    free(used);
    return count;
}

int main(void) {
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < 20; round++) {
        for (int64_t n = 1; n <= 15; n++) {
            int64_t count = count_arrangement(n);
            total += count;
            checksum = (checksum * 31 + count + round) % 1000000007;
        }
    }
    printf("n from 1 to 15, 20 rounds: total %lld, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
