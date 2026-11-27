// LeetCode #1839: Longest Substring Of All Vowels in Order -- the bench in C: the ★ arm over
// 1000 calls on 40 words of 10^5 vowels, built once, each vowel the one
// before it again, the next vowel, an `a`, or any vowel, each call's word
// drawn from the checksum so far. The arm reads the word's bytes where they
// are, so no call copies one.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_beautiful_substring(const char *word, int64_t n) {
    int64_t best = 0, length = 1, vowels = 1;
    for (int64_t i = 1; i < n; i++) {
        if (word[i] < word[i - 1]) {
            length = 1;
            vowels = 1;
        } else {
            length++;
            if (word[i] > word[i - 1]) vowels++;
        }
        if (vowels == 5 && length > best) best = length;
    }
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1839;
    const char vowels[] = "aeiou";
    char *words[40];
    for (int w = 0; w < 40; w++) {
        words[w] = malloc(100001);
        int64_t at = 0;
        for (int64_t i = 0; i < 100000; i++) {
            int64_t roll = next_random(&seed) % 10;
            if (roll < 4) {
                // the same vowel again
            } else if (roll < 8) {
                at = at + 1 < 4 ? at + 1 : 4;
            } else if (roll < 9) {
                at = 0;
            } else {
                at = next_random(&seed) % 5;
            }
            words[w][i] = vowels[at];
        }
        words[w][100000] = 0;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 1000; call++) {
        const char *w = words[(check + call) % 40];
        check = (check * 31 + longest_beautiful_substring(w, 100000)) % 1000000007;
    }
    printf("1000 calls: checksum %lld\n", (long long)check);
    return 0;
}
