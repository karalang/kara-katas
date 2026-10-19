// LeetCode 793 — Preimage Size of Factorial Zeroes Function: the bench,
// in C. Mirrors preimage_size_fzf.kara: binary search for the least x
// whose factorial has at least k zeroes at the end.
#include <stdint.h>
#include <stdio.h>

static int64_t zeroes(int64_t x) {
    int64_t count = 0;
    for (int64_t p = x / 5; p > 0; p /= 5) count += p;
    return count;
}

static int64_t preimage_size_fzf(int64_t k) {
    int64_t lo = 0, hi = 5 * k + 5;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (zeroes(mid) < k)
            lo = mid + 1;
        else
            hi = mid;
    }
    return zeroes(lo) == k ? 5 : 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 793, rounds = 4000000, fives = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t a = next_random(&seed);
        int64_t b = next_random(&seed);
        int64_t k = (a * 32768 + b) % 1000000001;
        int64_t answer = preimage_size_fzf(k);
        if (answer == 5) fives++;
        check = (check * 131 + k % 1000 + answer) % 1000000007;
    }
    printf("%lld values of k: %lld with five, checksum %lld\n", (long long)rounds, (long long)fives,
           (long long)check);
    return 0;
}
