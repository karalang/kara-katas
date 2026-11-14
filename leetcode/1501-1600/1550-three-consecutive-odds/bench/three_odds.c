// LeetCode #1550: Three Consecutive Odds -- bench: the ★ arm (the run of
// odd values) over 1000 arrays of 1 to 1000 values, each with its own
// chance of an odd value, built once, each asked 2000 times with one value
// raised by one before every ask, so no ask repeats the last. C mirror
// of three_odds.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int three_consecutive_odds(const int64_t *arr, int64_t n) {
    int64_t run = 0;
    for (int64_t i = 0; i < n; i++) {
        if (arr[i] % 2 == 1) {
            run++;
            if (run == 3) return 1;
        } else {
            run = 0;
        }
    }
    return 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1550;
    static int64_t *arrays[1000];
    static int64_t lengths[1000];
    for (int g = 0; g < 1000; g++) {
        int64_t length = (next_random(&seed) * 32768 + next_random(&seed)) % 1000 + 1;
        int64_t odds = next_random(&seed) % 101;
        arrays[g] = malloc(length * sizeof(int64_t));
        lengths[g] = length;
        for (int64_t i = 0; i < length; i++) {
            int odd = next_random(&seed) % 100 < odds;
            int64_t half = next_random(&seed) % 500;
            arrays[g][i] = odd ? 2 * half + 1 : 2 * half + 2;
        }
    }
    int64_t yes = 0, check = 0;
    for (int64_t pass = 0; pass < 2000; pass++) {
        for (int64_t g = 0; g < 1000; g++) {
            int64_t at = (pass * 7 + g) % lengths[g];
            arrays[g][at] += 1;
            if (three_consecutive_odds(arrays[g], lengths[g])) {
                yes++;
                check = (check * 31 + pass + g + 1) % 1000000007;
            }
        }
    }
    printf("2000 passes over 1000 arrays of up to 1000 values: %lld true, checksum %lld\n",
           (long long)yes, (long long)check);
    return 0;
}
