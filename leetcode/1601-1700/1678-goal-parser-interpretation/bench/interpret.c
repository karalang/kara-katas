// LeetCode #1678: Goal Parser Interpretation -- the bench's C mirror: the
// ★ arm on 100000 random commands of up to 100 characters, all drawn
// first, each interpreted 20 times. Each answer is malloc'd, as the other
// languages build a new string.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 100000
#define ROUNDS 20

// the answer, malloc'd, its length in `*len`
static char *interpret(const char *command, int64_t n, int64_t *len) {
    char *out = malloc((size_t)n + 1);
    int64_t i = 0, k = 0;
    while (i < n) {
        if (command[i] == 'G') {
            out[k++] = 'G';
            i += 1;
        } else if (command[i + 1] == ')') {
            out[k++] = 'o';
            i += 2;
        } else {
            out[k++] = 'a';
            out[k++] = 'l';
            i += 4;
        }
    }
    *len = k;
    return out;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1678;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static const char *tokens[3] = {"G", "()", "(al)"};
    static char commands[COUNT][101];
    static int64_t lengths[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t n = 0;
        int64_t length = next_random() % 100 + 1;
        for (;;) {
            const char *token = tokens[next_random() % 3];
            int64_t t = (int64_t)strlen(token);
            if (n + t > length) break;
            memcpy(commands[c] + n, token, (size_t)t);
            n += t;
        }
        if (n == 0) commands[c][n++] = 'G';
        commands[c][n] = '\0';
        lengths[c] = n;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t len;
            char *answer = interpret(commands[c], lengths[c], &len);
            total += len;
            check = (check * 31 + len + (unsigned char)answer[len - 1] + r) % 1000000007;
            free(answer);
        }
    }
    printf("%d commands, %d rounds: %lld letters, checksum %lld\n", COUNT, ROUNDS, (long long)total, (long long)check);
    return 0;
}
