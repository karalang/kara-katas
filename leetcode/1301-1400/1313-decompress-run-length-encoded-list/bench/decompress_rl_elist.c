// LeetCode #1313 bench, C: the ★ arm (the list read two numbers at a time,
// each pair's value pushed as many times as its count) on the same 100
// lists and 2000 passes. The answer grows by doubling, as the others' do,
// and is a fresh allocation each call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *decompress_rl_elist(const int64_t *nums, int64_t len, int64_t *out_len) {
    int64_t cap = 4, n = 0;
    int64_t *out = malloc(sizeof(int64_t) * (size_t)cap);
    for (int64_t i = 0; i < len; i += 2) {
        for (int64_t k = 0; k < nums[i]; k++) {
            if (n == cap) {
                cap *= 2;
                out = realloc(out, sizeof(int64_t) * (size_t)cap);
            }
            out[n++] = nums[i + 1];
        }
    }
    *out_len = n;
    return out;
}

static int64_t seed = 1313;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t lists[100][100];
    for (int l = 0; l < 100; l++) {
        for (int k = 0; k < 100; k++) lists[l][k] = 1 + next_random() % 100;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 2000; pass++) {
        for (int l = 0; l < 100; l++) {
            lists[l][2 * (check % 50)] = 1 + (check / 7) % 100;
            lists[l][2 * ((check / 11) % 50) + 1] = 1 + (check / 13) % 100;
            int64_t n;
            int64_t *got = decompress_rl_elist(lists[l], 100, &n);
            check = (check * 31 + n) % 1000000007;
            check = (check * 31 + got[check % n]) % 1000000007;
            check = (check * 31 + got[(check / 3) % n] + pass) % 1000000007;
            free(got);
        }
    }
    printf("2000 passes over 100 lists of 50 pairs: checksum %lld\n", (long long)check);
    return 0;
}
