// LeetCode 744 — Find Smallest Letter Greater Than Target, bench: the ★
// arm (binary search) on lists of 10000 sorted letters, many random
// targets each. Mirrors next_greatest_letter.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static char next_greatest_letter(const char *letters, int64_t len, char target) {
    int64_t lo = 0, hi = len;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (letters[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo == len ? letters[0] : letters[lo];
}

static int64_t seed = 744;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 60, n = 10000, queries = 100000;
    int64_t total = 0;
    for (int64_t r = 0; r < rounds; r++) {
        char *letters = malloc(n);
        int64_t c = 'a' + next_random() % 6;
        for (int64_t i = 0; i < n; i++) {
            if (next_random() % 500 == 0 && c < 'z') c++;
            letters[i] = (char)c;
        }
        if (letters[0] == letters[n - 1]) letters[n - 1] = letters[0] + 1;
        for (int64_t q = 0; q < queries; q++) {
            char target = (char)('a' + next_random() % 26);
            total += next_greatest_letter(letters, n, target);
        }
        free(letters);
    }
    printf("%lld rounds of 100000 queries on 10000 letters: answers sum to %lld\n",
           (long long)rounds, (long long)total);
    return 0;
}
