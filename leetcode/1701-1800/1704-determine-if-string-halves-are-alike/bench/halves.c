// LeetCode #1704: Determine if String Halves Are Alike -- the bench's C
// mirror: the ★ arm on 1000 random strings of 1000 letters, all drawn
// first, each answered 400 times.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 1000
#define ROUNDS 400
#define N 1000

// one pass: a vowel in the first half counted up and in the second down
static bool halves_are_alike(const char *s, int64_t n) {
    int64_t half = n / 2, balance = 0;
    for (int64_t i = 0; i < n; i++) {
        switch (s[i]) {
        case 'a': case 'e': case 'i': case 'o': case 'u':
        case 'A': case 'E': case 'I': case 'O': case 'U':
            balance += i < half ? 1 : -1;
            break;
        default:
            break;
        }
    }
    return balance == 0;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1704;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *vowels = "aeiouAEIOU";
    const char *consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ";
    int64_t nv = (int64_t)strlen(vowels), nc = (int64_t)strlen(consonants);
    char *strings = malloc((size_t)COUNT * N);
    for (int c = 0; c < COUNT; c++) {
        // each letter a vowel with a chance of its string's own, 0 to 10 in 10
        int64_t lean = next_random() % 11;
        for (int64_t i = 0; i < N; i++) {
            char b;
            if (next_random() % 10 < lean) {
                b = vowels[next_random() % nv];
            } else {
                b = consonants[next_random() % nc];
            }
            strings[(int64_t)c * N + i] = b;
        }
    }
    int64_t alike = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            bool answer = halves_are_alike(strings + (int64_t)c * N, N);
            if (answer) {
                alike++;
            }
            check = (check * 31 + (answer ? 1 : 2) + r) % 1000000007;
        }
    }
    printf("%d strings of %d letters, %d rounds: %lld alike, checksum %lld\n", COUNT, N, ROUNDS, (long long)alike, (long long)check);
    free(strings);
    return 0;
}
