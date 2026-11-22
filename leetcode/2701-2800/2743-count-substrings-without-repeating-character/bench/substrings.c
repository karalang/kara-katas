// LeetCode #2743: Count Substrings Without Repeating Character -- the
// bench (substrings.kara in C): a window with each letter's last place.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t number_of_special_substrings(const unsigned char *s, int64_t n) {
    int64_t last[26];
    for (int i = 0; i < 26; i++) last[i] = -1;
    int64_t start = 0, count = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t letter = s[i] - 'a';
        if (last[letter] + 1 > start) start = last[letter] + 1;
        last[letter] = i;
        count += i - start + 1;
    }
    return count;
}

static int64_t seed = 2743;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 20, n = 100000, rounds = 300;
    unsigned char *words = malloc(count * n);
    for (int64_t c = 0; c < count; c++) {
        int64_t k = next_random() % 22 + 5;
        for (int64_t i = 0; i < n; i++) words[c * n + i] = (unsigned char)('a' + next_random() % k);
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t found = number_of_special_substrings(words + c * n, n);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    printf("%lld words of %lld letters, %lld rounds: counts sum to %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)sum, (long long)check);
    free(words);
    return 0;
}
