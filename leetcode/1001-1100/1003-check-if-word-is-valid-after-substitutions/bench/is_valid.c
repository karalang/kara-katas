// Benchmark: LeetCode #1003 Check If Word Is Valid After Substitutions --
// the ★ arm, a stack, on strings of 19998 letters, LeetCode's longest.
// Mirrors is_valid.kara, .rs, .py and go-seq/.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool is_valid(const char *s) {
    size_t n = strlen(s);
    char *stack = malloc(n + 1);
    size_t k = 0;
    for (size_t i = 0; i < n; i++) {
        stack[k++] = s[i];
        if (k >= 3 && stack[k - 3] == 'a' && stack[k - 2] == 'b' && stack[k - 1] == 'c') k -= 3;
    }
    free(stack);
    return k == 0;
}

static int64_t seed = 1003;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// a valid string of `pieces` pieces, made left to right: each step
// either begins a new piece with its a or writes the next letter of the
// latest piece begun, at random
static void random_valid(int64_t pieces, char *xs) {
    static char waiting[20000];
    size_t n = 0, w = 0;
    int64_t left = pieces;
    while (left > 0 || w > 0) {
        if (left > 0 && (w == 0 || next_random() % 2 == 0)) {
            xs[n++] = 'a';
            waiting[w++] = 'b';
            left--;
        } else {
            char c = waiting[w - 1];
            xs[n++] = c;
            if (c == 'b') waiting[w - 1] = 'c';
            else w--;
        }
    }
    xs[n] = 0;
}

int main(void) {
    int rounds = 250;
    // 20 strings of 6666 pieces, 19998 letters; the odd ones with one
    // letter changed
    const char letters[3] = {'a', 'b', 'c'};
    static char strings[20][19999];
    for (int t = 0; t < 20; t++) {
        random_valid(6666, strings[t]);
        if (t % 2 == 1) {
            int64_t at = next_random() % 19998;
            strings[t][at] = letters[(next_random() % 2 + 1 + strings[t][at] - 97) % 3];
        }
    }
    int64_t valid = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t v = is_valid(strings[(r + i) % 20]) ? 1 : 0;
            valid += v;
            check = (check * 31 + v + i + 1) % 1000000007;
        }
    }
    printf("%d rounds over 20 strings of 19998 letters: %lld valid, checksum %lld\n", rounds,
           (long long)valid, (long long)check);
    return 0;
}
