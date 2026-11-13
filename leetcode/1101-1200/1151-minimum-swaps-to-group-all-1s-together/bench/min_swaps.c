// LeetCode #1151: Minimum Swaps to Group All 1's Together -- the C mirror
// of the ★ arm: a window as long as the count of ones slides along the
// list, and the answer is the count less the most ones it holds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_swaps(const int64_t *data, int64_t n) {
    int64_t k = 0;
    for (int64_t i = 0; i < n; i++) k += data[i];
    if (k == 0) return 0;
    int64_t inside = 0;
    for (int64_t i = 0; i < k; i++) inside += data[i];
    int64_t most = inside;
    for (int64_t i = k; i < n; i++) {
        inside += data[i] - data[i - k];
        if (inside > most) most = inside;
    }
    return k - most;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1151;
    int64_t *lists[16];
    for (int l = 0; l < 16; l++) {
        int64_t ones = 1 + l % 7;
        lists[l] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) lists[l][i] = next_random(&seed) % 8 < ones ? 1 : 0;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 3000; r++) {
        int l = r % 16;
        for (int j = 0; j < 64; j++) {
            int64_t at = next_random(&seed) * 3;
            lists[l][at] = 1 - lists[l][at];
        }
        int64_t s = min_swaps(lists[l], 100000);
        total += s;
        check = (check * 31 + s) % 1000000007;
    }
    printf("3000 rounds over 16 lists of 100000 bits: swaps total %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int l = 0; l < 16; l++) free(lists[l]);
    return 0;
}
