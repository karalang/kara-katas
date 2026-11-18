// LeetCode #2264: Largest 3-Same-Digit Number in String -- C mirror of
// the ★ arm (good.kara): one pass over the bytes, the largest digit seen
// three times running, written three times into a fresh string or "".
// Output is byte-identical to good.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *largest_good_integer(const char *num, int n) {
    int best = -1;
    for (int i = 2; i < n; i++) {
        if (num[i - 2] == num[i] && num[i - 1] == num[i]) {
            if (best < 0 || num[i] > best) best = num[i];
        }
    }
    char *s = malloc(4);
    if (best < 0) {
        s[0] = 0;
    } else {
        s[0] = s[1] = s[2] = (char)best;
        s[3] = 0;
    }
    return s;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2264;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    char *num = malloc(1001);
    for (int t = 0; t < 2000; t++) {
        int64_t digits = t % 2 == 0 ? 4 : 10;
        for (int i = 0; i < 1000; i++) num[i] = (char)('0' + next_random() % digits);
        num[1000] = 0;
        char *good = largest_good_integer(num, 1000);
        int64_t score = good[0] == 0 ? 1000 : strtoll(good, NULL, 10);
        free(good);
        check = (check * 31 + score) % 1000000007;
    }
    free(num);
    printf("2000 numbers of 1000: checksum %lld\n", (long long)check);
    return 0;
}
