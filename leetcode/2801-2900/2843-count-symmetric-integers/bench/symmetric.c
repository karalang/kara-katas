// LeetCode #2843: Count Symmetric Integers -- the bench, mirrored from
// symmetric.kara: each number written out with snprintf and its halves'
// digits summed in place.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static bool symmetric(int64_t x) {
    char text[24];
    int n = snprintf(text, sizeof text, "%lld", (long long)x);
    if (n % 2 == 1) return false;
    int64_t first = 0, last = 0;
    for (int i = 0; i < n / 2; i++) first += text[i] - '0';
    for (int i = n / 2; i < n; i++) last += text[i] - '0';
    return first == last;
}

static int64_t count_symmetric_integers(int64_t low, int64_t high) {
    int64_t count = 0;
    for (int64_t x = low; x <= high; x++)
        if (symmetric(x)) count++;
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 5000, rounds = 2;
    int64_t seed = 2843, lows[5000], highs[5000];
    for (long c = 0; c < count; c++) {
        int64_t a = next_random(&seed) % 10000 + 1;
        int64_t b = next_random(&seed) % 10000 + 1;
        lows[c] = a < b ? a : b;
        highs[c] = a < b ? b : a;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            int64_t got = count_symmetric_integers(lows[c], highs[c]);
            total += got;
            check = (check * 31 + got + r) % 1000000007;
        }
    }
    printf("%ld ranges, %ld rounds: %lld in all, checksum %lld\n", count, rounds, (long long)total, (long long)check);
    return 0;
}
