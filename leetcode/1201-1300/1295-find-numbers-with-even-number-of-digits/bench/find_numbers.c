// LeetCode #1295 bench: the ★ arm over 200 arrays of 500 numbers up to 10^5,
// built once; then 500 passes, each setting one number of every array from
// the checksum so far and answering it.
#include <stdint.h>
#include <stdio.h>

enum { ARRAYS = 200, LEN = 500 };

static int64_t find_numbers(const int64_t *nums, int n) {
    int64_t even = 0;
    for (int i = 0; i < n; i++) {
        int64_t digits = 0;
        for (int64_t rest = nums[i]; rest > 0; rest /= 10) {
            digits++;
        }
        if (digits % 2 == 0) {
            even++;
        }
    }
    return even;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t arrays[ARRAYS][LEN];

int main(void) {
    int64_t seed = 1295;
    for (int a = 0; a < ARRAYS; a++) {
        for (int i = 0; i < LEN; i++) {
            int64_t digits = next_random(&seed) % 6 + 1;
            int64_t low = 1;
            for (int64_t d = 1; d < digits; d++) {
                low *= 10;
            }
            if (digits == 6) {
                arrays[a][i] = 100000;
            } else {
                int64_t r = next_random(&seed);
                arrays[a][i] = low + (r * 32768 + next_random(&seed)) % (9 * low);
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int a = 0; a < ARRAYS; a++) {
            arrays[a][check % 500] = 1 + check % 100000;
            check = (check * 31 + find_numbers(arrays[a], LEN) + p) % 1000000007;
        }
    }
    printf("500 passes over 200 arrays of 500: checksum %lld\n", (long long)check);
    return 0;
}
