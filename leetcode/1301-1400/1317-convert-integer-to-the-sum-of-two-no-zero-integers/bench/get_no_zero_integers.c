// LeetCode #1317 bench, C mirror of the Kāra bench: the ★ arm (the first
// number tried from 1 up, each pair's digits read off by `% 10` and `/ 10`,
// until neither has a 0) on every n from 2 to 10^4; 300 passes, each
// starting its walk through the range at a place chosen by the checksum so
// far and folding both numbers of every answer into it. Each answer is a
// fresh two-number array, a `malloc`, as the Kāra arm returns a fresh `Vec`.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool has_zero(int64_t x) {
    int64_t rest = x;
    while (rest > 0) {
        if (rest % 10 == 0) return true;
        rest /= 10;
    }
    return false;
}

static int64_t *get_no_zero_integers(int64_t n) {
    int64_t a = 1;
    while (has_zero(a) || has_zero(n - a)) a++;
    int64_t *v = malloc(2 * sizeof(int64_t));
    v[0] = a;
    v[1] = n - a;
    return v;
}

int main(void) {
    int64_t check = 0;
    for (int64_t pass = 0; pass < 300; pass++) {
        int64_t start = check % 9999;
        for (int64_t k = 0; k < 9999; k++) {
            int64_t n = 2 + (start + k) % 9999;
            int64_t *v = get_no_zero_integers(n);
            check = (check * 31 + v[0] * 7 + v[1] + pass) % 1000000007;
            free(v);
        }
    }
    printf("300 passes over every n from 2 to 10^4: checksum %lld\n", (long long)check);
    return 0;
}
