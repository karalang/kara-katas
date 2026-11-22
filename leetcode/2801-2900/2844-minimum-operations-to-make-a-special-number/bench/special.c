// LeetCode #2844: Minimum Operations to Make a Special Number -- the
// bench, mirrored from special.kara: one pass from the right, ending
// the number at the first 0 or 5 after a 0, or 2 or 7 after a 5.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimum_operations(const char *digits, int64_t n) {
    bool zero = false, five = false;
    for (int64_t i = n - 1; i >= 0; i--) {
        char d = digits[i];
        if ((zero && (d == '0' || d == '5')) || (five && (d == '2' || d == '7'))) return n - i - 2;
        if (d == '0') zero = true;
        if (d == '5') five = true;
    }
    return zero ? n - 1 : n;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 100000, rounds = 300;
    int64_t seed = 2844;
    char *text = malloc(count * 100);
    int64_t *starts = malloc(count * sizeof(int64_t)), *lens = malloc(count * sizeof(int64_t));
    int64_t at = 0;
    for (long c = 0; c < count; c++) {
        int64_t n = next_random(&seed) % 100 + 1;
        starts[c] = at;
        lens[c] = n;
        for (int64_t i = 0; i < n; i++) {
            int64_t low = (i == 0 && n > 1) ? 1 : 0;
            text[at++] = (char)(48 + low + next_random(&seed) % (10 - low));
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            int64_t ops = minimum_operations(text + starts[c], lens[c]);
            total += ops;
            check = (check * 31 + ops + r) % 1000000007;
        }
    }
    printf("%ld numbers, %ld rounds: %lld operations, checksum %lld\n", count, rounds, (long long)total, (long long)check);
    free(text);
    free(starts);
    free(lens);
    return 0;
}
