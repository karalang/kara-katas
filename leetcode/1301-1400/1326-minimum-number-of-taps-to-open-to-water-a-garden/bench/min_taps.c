// LeetCode #1326 bench, C mirror of the Kāra bench: the ★ arm (each tap
// turned into how far right it waters from its leftmost point, then the
// garden crossed as a jump game) on 20 gardens of 10^4 built once; then 300
// passes, each setting one tap of every garden from the checksum so far,
// answering it and folding the answer plus the pass into the checksum. Each
// call takes a fresh table, a `calloc`, as the Kāra arm takes a fresh `Vec`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t min_taps(int32_t n32, const int32_t *ranges) {
    int64_t n = n32;
    int64_t *farthest = calloc((size_t)(n + 1), sizeof(int64_t));
    for (int64_t i = 0; i <= n; i++) {
        int64_t r = ranges[i];
        int64_t left = i - r > 0 ? i - r : 0;
        int64_t right = i + r < n ? i + r : n;
        if (right > farthest[left]) farthest[left] = right;
    }
    int64_t taps = 0, watered = 0, next = 0;
    for (int64_t x = 0; x < n; x++) {
        if (farthest[x] > next) next = farthest[x];
        if (x == watered) {
            if (next <= x) {
                free(farthest);
                return -1;
            }
            taps++;
            watered = next;
        }
    }
    free(farthest);
    return (int32_t)taps;
}

static int64_t seed = 1326;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 10000;
    static int32_t gardens[20][10001];
    for (int t = 0; t < 20; t++) {
        int64_t open = t % 4 == 0 ? 1 : t % 4 == 1 ? 3 : t % 4 == 2 ? 10 : 30;
        for (int64_t i = 0; i <= n; i++) {
            int64_t r = next_random() % open == 0 ? 1 + next_random() % 100 : 0;
            gardens[t][i] = (int32_t)r;
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 300; pass++) {
        for (int t = 0; t < 20; t++) {
            gardens[t][check % (n + 1)] = (int32_t)((check / 7) % 101);
            int64_t taps = min_taps((int32_t)n, gardens[t]);
            check = (check * 31 + taps + 1 + pass) % 1000000007;
        }
    }
    printf("300 passes over 20 gardens of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
