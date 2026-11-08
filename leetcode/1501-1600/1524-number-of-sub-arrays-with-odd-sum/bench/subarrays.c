// LeetCode #1524: Number of Sub-arrays With Odd Sum -- bench: the ★ arm
// over 100 random arrays of 1 to 100000 numbers from 1 to 100, built once
// and answered 20 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_of_subarrays(const int64_t *arr, int64_t n) {
    const int64_t modulus = 1000000007;
    int64_t odd = 0, even = 1, sum = 0, answer = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += arr[i];
        if (sum % 2 == 1) {
            answer = (answer + even) % modulus;
            odd++;
        } else {
            answer = (answer + odd) % modulus;
            even++;
        }
    }
    return answer;
}

static int64_t seed = 1524;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 100 };
    static int64_t *arrays[COUNT];
    static int64_t lens[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t hi = next_random();
        int64_t n = (hi * 32768 + next_random()) % 100000 + 1;
        arrays[c] = malloc((size_t)n * sizeof(int64_t));
        lens[c] = n;
        for (int64_t i = 0; i < n; i++) {
            arrays[c][i] = next_random() % 100 + 1;
        }
    }
    int64_t check = 0;
    for (int pass = 0; pass < 20; pass++) {
        for (int c = 0; c < COUNT; c++) {
            check = mix(check, num_of_subarrays(arrays[c], lens[c]));
        }
    }
    printf("20 passes over 100 arrays of up to 100000 numbers: checksum %lld\n", (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(arrays[c]);
    }
    return 0;
}
