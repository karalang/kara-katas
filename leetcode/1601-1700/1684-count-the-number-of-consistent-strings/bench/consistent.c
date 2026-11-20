// LeetCode #1684: Count the Number of Consistent Strings -- the bench's C
// mirror: the ★ arm on 100 random problems of 10000 words, all drawn
// first, each answered 20 times.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define COUNT 100
#define SIZE 10000
#define ROUNDS 20

// the words of one problem, each NUL-terminated in 11 bytes
static int32_t count_consistent(const char *allowed, char (*words)[11], int n) {
    bool ok[26];
    memset(ok, 0, sizeof ok);
    for (const char *p = allowed; *p; p++) ok[*p - 'a'] = true;
    int32_t count = 0;
    for (int w = 0; w < n; w++) {
        bool all = true;
        for (const char *p = words[w]; *p; p++) {
            if (!ok[*p - 'a']) {
                all = false;
                break;
            }
        }
        if (all) count += 1;
    }
    return count;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1684;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char allowed[COUNT][27];
    static char words[COUNT][SIZE][11];
    for (int c = 0; c < COUNT; c++) {
        int k = 0;
        for (int b = 0; b < 26; b++) {
            if (next_random() % 8 != 0) allowed[c][k++] = (char)('a' + b);
        }
        if (k == 0) allowed[c][k++] = 'a';
        allowed[c][k] = '\0';
        for (int w = 0; w < SIZE; w++) {
            int64_t length = next_random() % 10 + 1;
            for (int64_t i = 0; i < length; i++) words[c][w][i] = (char)('a' + next_random() % 26);
            words[c][w][length] = '\0';
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int32_t answer = count_consistent(allowed[c], words[c], SIZE);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d words, %d rounds: %lld consistent, checksum %lld\n", COUNT, SIZE, ROUNDS, (long long)total, (long long)check);
    return 0;
}
