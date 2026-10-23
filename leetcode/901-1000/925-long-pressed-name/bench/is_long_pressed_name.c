// LeetCode #925: Long Pressed Name -- bench: two pointers.
// Mirrors is_long_pressed_name.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool is_long_pressed_name(const char *a, int64_t n, const char *b, int64_t m) {
    int64_t i = 0;
    for (int64_t j = 0; j < m; j++) {
        if (i < n && a[i] == b[j]) i++;
        else if (j > 0 && b[j] == b[j - 1]) continue;
        else return false;
    }
    return i == n;
}

static int64_t seed = 925;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 150, count = 1000, n = 400;
    // count names of 400 letters from "abc", each typed with about one key
    // in four held down for up to three more presses, and every third one
    // mistyped once
    char **names = malloc(count * sizeof(char *));
    char **typings = malloc(count * sizeof(char *));
    int64_t *lengths = malloc(count * sizeof(int64_t));
    for (int64_t p = 0; p < count; p++) {
        names[p] = malloc(n);
        typings[p] = malloc(4 * n);
        int64_t m = 0;
        for (int64_t k = 0; k < n; k++) {
            char c = (char)('a' + next_random() % 3);
            names[p][k] = c;
            int64_t extra = next_random() % 4 == 0 ? 1 + next_random() % 3 : 0;
            for (int64_t e = 0; e < 1 + extra; e++) typings[p][m++] = c;
        }
        if (p % 3 == 0) {
            int64_t at = next_random() % m;
            typings[p][at] = (char)('a' + next_random() % 3);
        }
        lengths[p] = m;
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every pair, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            int64_t p = (r + i) % count;
            if (is_long_pressed_name(names[p], n, typings[p], lengths[p])) {
                yes++;
                check = (check * 1000003 + p + 1) % 1000000007;
            }
        }
    }
    printf("%lld rounds over %lld names of 400 letters: %lld long pressed, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)yes, (long long)check);
    for (int64_t p = 0; p < count; p++) {
        free(names[p]);
        free(typings[p]);
    }
    free(names);
    free(typings);
    free(lengths);
    return 0;
}
