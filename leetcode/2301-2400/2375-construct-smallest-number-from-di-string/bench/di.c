// LeetCode #2375: Construct Smallest Number From DI String -- the bench,
// the ★ arm in C: the digits 1 to n + 1 pushed on a stack, emptied at
// every I and at the end, so each run of D's comes out falling. The
// result and the stack are allocated in each call, as the other
// languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *smallest_number(const char *pattern) {
    size_t n = strlen(pattern);
    char *out = malloc(n + 2);
    char *stack = malloc(n + 1);
    size_t len = 0, top = 0;
    for (size_t i = 0; i <= n; i++) {
        stack[top++] = (char)('1' + i);
        if (i == n || pattern[i] == 'I') {
            while (top > 0) {
                out[len++] = stack[--top];
            }
        }
    }
    out[len] = 0;
    free(stack);
    return out;
}

int main(void) {
    // every pattern of 1 to 8 letters, 510 in all
    char patterns[510][9];
    int count = 0;
    for (int n = 1; n < 9; n++) {
        for (int mask = 0; mask < 1 << n; mask++) {
            for (int i = 0; i < n; i++) {
                patterns[count][i] = (mask >> i) & 1 ? 'D' : 'I';
            }
            patterns[count][n] = 0;
            count++;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 2000; p++) {
        for (int k = 0; k < count; k++) {
            char *number = smallest_number(patterns[k]);
            for (char *b = number; *b; b++) {
                check = (check * 31 + (*b - '0') + p) % 1000000007;
            }
            free(number);
        }
    }
    printf("2000 passes over 510 patterns: checksum %lld\n", (long long)check);
    return 0;
}
