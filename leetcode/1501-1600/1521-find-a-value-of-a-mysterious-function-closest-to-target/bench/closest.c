// LeetCode #1521: Find a Value of a Mysterious Function Closest to Target
// -- bench: the ★ arm over 2000 random arrays of 1 to 4000 numbers, built
// once and answered 3 times. Each place's list of ANDs is a fresh
// allocation, as the other languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t closest_to_target(const int64_t *arr, int64_t n, int64_t target) {
    int64_t best = llabs(arr[0] - target);
    int64_t *ends = NULL;
    int64_t ends_len = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = arr[i];
        int64_t *next = malloc((size_t)(ends_len + 1) * sizeof(int64_t));
        int64_t len = 0;
        next[len++] = x;
        for (int64_t j = 0; j < ends_len; j++) {
            int64_t w = ends[j] & x;
            if (w != next[len - 1]) {
                next[len++] = w;
            }
        }
        for (int64_t j = 0; j < len; j++) {
            int64_t d = llabs(next[j] - target);
            if (d < best) {
                best = d;
            }
        }
        free(ends);
        ends = next;
        ends_len = len;
    }
    free(ends);
    return best;
}

static int64_t seed = 1521;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 2000 };
    static int64_t *arrays[COUNT];
    static int64_t lens[COUNT];
    static int64_t targets[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t n = next_random() % 4000 + 1;
        int64_t base = next_random() % 1000000 + 1;
        int64_t *arr = malloc((size_t)n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            int64_t x;
            if (next_random() % 2 == 0) {
                int64_t hi = next_random();
                x = base & (hi * 32768 + next_random());
            } else {
                x = next_random() * 32 % 1000000;
            }
            arr[i] = x < 1 ? 1 : x;
        }
        int64_t hi = next_random();
        targets[c] = (hi * 32768 + next_random()) % 1000001;
        arrays[c] = arr;
        lens[c] = n;
    }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 3; pass++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = closest_to_target(arrays[c], lens[c], targets[c]);
            total += answer;
            check = mix(check, answer);
        }
    }
    printf("3 passes over 2000 arrays of up to 4000 numbers: distances sum to %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int c = 0; c < COUNT; c++) {
        free(arrays[c]);
    }
    return 0;
}
