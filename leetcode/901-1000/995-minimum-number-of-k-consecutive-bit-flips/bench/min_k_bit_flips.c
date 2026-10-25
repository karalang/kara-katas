// Benchmark: LeetCode #995 Minimum Number of K Consecutive Bit Flips --
// the ★ arm, the greedy with a running parity, on random arrays of
// 100000 bits, LeetCode's largest. Mirrors min_k_bit_flips.kara, .rs,
// .py and go-seq/.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_k_bit_flips(const int64_t *nums, int64_t n, int64_t k) {
    bool *ends = calloc((size_t)n + 1, sizeof(bool));
    bool flipped = false;
    int64_t flips = 0;
    for (int64_t i = 0; i < n; i++) {
        if (ends[i]) flipped = !flipped;
        if ((nums[i] == 1) == flipped) {
            if (i + k > n) {
                free(ends);
                return -1;
            }
            flips++;
            flipped = !flipped;
            ends[i + k] = true;
        }
    }
    free(ends);
    return flips;
}

static int64_t seed = 995;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 50;
    // ten arrays of random bits and ten of ones put through random flips
    // of 1 to 100 bits, which can be made all ones again
    int64_t *arrays[20], ks[20];
    for (int a = 0; a < 20; a++) {
        int64_t *nums = malloc(sizeof(int64_t) * 100000);
        if (a % 2 == 0) {
            for (int i = 0; i < 100000; i++) nums[i] = next_random() % 2;
            ks[a] = 1 + next_random() % 100;
        } else {
            int64_t k = 1 + next_random() % 100;
            for (int i = 0; i < 100000; i++) nums[i] = 1;
            for (int64_t i = 0; i < 100000 - k + 1; i++) {
                if (next_random() % 4 == 0) {
                    for (int64_t j = i; j < i + k; j++) nums[j] = 1 - nums[j];
                }
            }
            ks[a] = k;
        }
        arrays[a] = nums;
    }
    int64_t stuck = 0, total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int a = (r + i) % 20;
            int64_t got = min_k_bit_flips(arrays[a], 100000, ks[a]);
            if (got < 0) stuck++;
            else total += got;
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    printf("%d rounds over 20 arrays of 100000 bits: %lld impossible, %lld flips, checksum %lld\n",
           rounds, (long long)stuck, (long long)total, (long long)check);
    return 0;
}
