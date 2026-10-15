// Benchmark for #657: walk the moves, as the Kara ★ arm.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool judge_circle(const char *moves, int64_t n) {
    int64_t x = 0, y = 0;
    for (int64_t i = 0; i < n; i++) {
        switch (moves[i]) {
        case 'U': y += 1; break;
        case 'D': y -= 1; break;
        case 'L': x -= 1; break;
        default: x += 1; break;
        }
    }
    return x == 0 && y == 0;
}

static int64_t seed = 657;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *random_moves(int64_t n, bool balanced) {
    static const char letters[] = "UDLR";
    char *s = malloc(n + 1);
    int64_t len = 0;
    if (balanced) {
        for (int64_t k = 0; k < n / 2; k++) {
            int64_t pair = next_random() % 2;
            s[len++] = letters[pair * 2];
            s[len++] = letters[pair * 2 + 1];
        }
        for (int64_t i = len - 1; i > 0; i--) {
            int64_t j = next_random() % (i + 1);
            char t = s[i];
            s[i] = s[j];
            s[j] = t;
        }
    } else {
        for (int64_t k = 0; k < n; k++) s[len++] = letters[next_random() % 4];
    }
    s[len] = 0;
    return s;
}

int main(void) {
    int inputs = 8, rounds = 100;
    int64_t n = 1000000;
    char *strings[8];
    for (int k = 0; k < inputs; k++) strings[k] = random_moves(n, k % 2 == 0);
    int64_t back = 0, checksum = 0;
    for (int r = 0; r < rounds; r++) {
        int64_t pick = (r * 3) % inputs;
        bool at = judge_circle(strings[pick], n);
        if (at) back++;
        checksum = (checksum * 31 + pick * 2 + (at ? 1 : 0)) % 1000000007;
    }
    printf("%d strings of 1000000, %d rounds: %lld back, checksum %lld\n", inputs, rounds,
           (long long)back, (long long)checksum);
    for (int k = 0; k < inputs; k++) free(strings[k]);
    return 0;
}
