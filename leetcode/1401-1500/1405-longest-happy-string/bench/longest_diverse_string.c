// LeetCode #1405 bench, C: the same greedy, a sort of the three letters
// before each one placed, workload and checksum as
// longest_diverse_string.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int32_t n;
    char ch;
} Left;

// most left first, stable as the Kara sort is
static void sort_left(Left *left) {
    for (int i = 1; i < 3; i++) {
        Left x = left[i];
        int j = i - 1;
        while (j >= 0 && left[j].n < x.n) {
            left[j + 1] = left[j];
            j--;
        }
        left[j + 1] = x;
    }
}

static int longest_diverse_string(int32_t a, int32_t b, int32_t c, char *out) {
    Left left[3] = {{a, 'a'}, {b, 'b'}, {c, 'c'}};
    int len = 0;
    for (;;) {
        sort_left(left);
        int placed = 0;
        for (int i = 0; i < 3; i++) {
            if (left[i].n == 0) {
                break;
            }
            char ch = left[i].ch;
            if (len >= 2 && out[len - 1] == ch && out[len - 2] == ch) {
                continue;
            }
            out[len++] = ch;
            left[i].n--;
            placed = 1;
            break;
        }
        if (!placed) {
            return len;
        }
    }
}

int main(void) {
    int64_t seed = 1405, check = 0;
    char out[320];
    for (int r = 0; r < 20000; r++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int32_t a = (int32_t)(seed / 65536 % 101);
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int32_t b = (int32_t)(seed / 65536 % 101);
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int32_t c = (int32_t)(1 + seed / 65536 % 100);
        int len = longest_diverse_string(a, b, c, out);
        for (int i = 0; i < len; i++) {
            check = (check * 131 + out[i]) % 1000000007;
        }
    }
    printf("20000 strings of up to 300 letters: checksum %lld\n", (long long)check);
    return 0;
}
