// LeetCode #2472: Maximum Number of Non-overlapping Palindrome Substrings
// -- the bench, the ★ arm in C: the greedy over starts, a palindrome of
// `k` letters from here taken first, else one of `k + 1`, each checked by
// two indices walked inward. The strings are `char` arrays.
#include <stdint.h>
#include <stdio.h>

static int is_palindrome(const char *c, int64_t lo, int64_t hi) {
    while (lo < hi) {
        if (c[lo] != c[hi]) return 0;
        lo++;
        hi--;
    }
    return 1;
}

static int64_t max_palindromes(const char *c, int64_t n, int64_t k) {
    int64_t count = 0, i = 0;
    while (i + k <= n) {
        if (is_palindrome(c, i, i + k - 1)) {
            count++;
            i += k;
        } else if (i + k < n && is_palindrome(c, i, i + k)) {
            count++;
            i += k + 1;
        } else {
            i++;
        }
    }
    return count;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2472;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define N 2000

static char texts[20][N];

int main(void) {
    // 20 strings of 2000 letters from "ab" built once; then 2400 passes,
    // each setting one letter of every string from the checksum so far,
    // then answering it with `k` from 2 to 6 by the pass, folding the
    // count plus the pass into the checksum
    const char letters[2] = {'a', 'b'};
    for (int a = 0; a < 20; a++)
        for (int i = 0; i < N; i++) texts[a][i] = letters[next_random() % 2];
    int64_t check = 0;
    for (int64_t p = 0; p < 2400; p++) {
        int64_t k = 2 + p % 5;
        for (int64_t a = 0; a < 20; a++) {
            texts[a][(check + a) % N] = letters[check % 2];
            check = (check * 31 + max_palindromes(texts[a], N, k) + p) % 1000000007;
        }
    }
    printf("2400 passes over 20 strings of 2000: checksum %lld\n", (long long)check);
    return 0;
}
