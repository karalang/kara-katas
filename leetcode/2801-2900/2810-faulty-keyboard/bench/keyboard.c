// LeetCode #2810: Faulty Keyboard -- the bench in C: the ★ arm over 20000
// strings of 100 letters, about a fifth of them i, all drawn first, then
// each typed 10 times; the screen a heap buffer turned round into a fresh
// one at each i, as the other languages collect a new string.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20000
#define M 100

static int64_t seed = 2810;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *final_string(const char *s) {
    char *screen = malloc(M + 1);
    size_t len = 0;
    for (; *s; s++) {
        if (*s == 'i') {
            char *turned = malloc(M + 1);
            for (size_t k = 0; k < len; k++) turned[k] = screen[len - 1 - k];
            free(screen);
            screen = turned;
        } else {
            screen[len++] = *s;
        }
    }
    screen[len] = 0;
    return screen;
}

static int64_t digest(const char *s) {
    int64_t h = 0;
    for (; *s; s++) h = (h * 131 + (unsigned char)*s) % 1000000007;
    return h;
}

static char cases[COUNT][M + 1];

int main(void) {
    int rounds = 10;
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    for (int c = 0; c < COUNT; c++) {
        for (int k = 0; k < M; k++) {
            int64_t r = next_random() % 125;
            cases[c][k] = r < 25 ? 'i' : letters[r % 26];
        }
        cases[c][M] = 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            char *out = final_string(cases[c]);
            total += (int64_t)strlen(out);
            check = (check * 31 + digest(out) + r) % 1000000007;
            free(out);
        }
    }
    printf("%d strings of 100, %d rounds: lengths sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
