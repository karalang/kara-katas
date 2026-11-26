// LeetCode #1461 bench in C: the ★ arm (the last k digits kept as a
// number, each window marked once) on the same 20 strings of 5 * 10^5
// digits, k from 11 to 20.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 500000

static int has_all_codes(const char *s, int n, int k) {
    int need = 1 << k;
    char *seen = calloc(need, 1);
    int found = 0, window = 0, all = 0;
    for (int i = 0; i < n; i++) {
        window = ((window << 1) | (s[i] - '0')) & (need - 1);
        if (i + 1 >= k && !seen[window]) {
            seen[window] = 1;
            if (++found == need) {
                all = 1;
                break;
            }
        }
    }
    free(seen);
    return all;
}

static int64_t seed = 1461;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char texts[20][N];
    for (int t = 0; t < 20; t++)
        for (int i = 0; i < N; i++) texts[t][i] = next_random() % 2 == 0 ? '0' : '1';
    char *s = malloc(N + 1);
    int64_t check = 0;
    for (int t = 0; t < 20; t++) {
        for (int k = 11; k <= 20; k++) {
            int at = (int)(check % N);
            texts[t][at] = texts[t][at] == '0' ? '1' : '0';
            memcpy(s, texts[t], N);
            s[N] = 0;
            int all = has_all_codes(s, N, k);
            check = (check * 31 + all + k) % 1000000007;
        }
    }
    free(s);
    printf("20 strings of 5 * 10^5 digits, k from 11 to 20: checksum %lld\n", (long long)check);
    return 0;
}
