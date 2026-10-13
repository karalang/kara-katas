// Benchmark for #503 in C: the ★ arm (a stack of indices, twice around);
// see ../next_greater_elements.kara. The answer and the stack are fresh
// malloc'd arrays on every call, as the Kāra arm's are fresh Vecs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *next_greater_elements(const int64_t *nums, int64_t n) {
    int64_t *answer = malloc(n * sizeof *answer);
    int64_t *waiting = malloc(n * sizeof *waiting);
    int64_t top = 0;
    for (int64_t i = 0; i < n; i++) answer[i] = -1;
    for (int64_t i = 0; i < 2 * n; i++) {
        int64_t x = nums[i % n];
        while (top > 0 && nums[waiting[top - 1]] < x) {
            answer[waiting[top - 1]] = x;
            top--;
        }
        if (i < n) waiting[top++] = i;
    }
    free(waiting);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 120 arrays of 10,000 numbers (the problem's most), from 0 to 9,
    // from the whole range -10^9 to 10^9, or falling, in turn; built
    // once. Then each array is solved 100 times, the sum of its
    // answers folded into a checksum.
    const int64_t arrays = 120, rounds = 100, n = 10000;
    int64_t seed = 503;
    int64_t *all = malloc(arrays * n * sizeof *all);
    for (int64_t c = 0; c < arrays; c++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t v;
            if (c % 3 == 0) {
                v = next_random(&seed) % 10;
            } else if (c % 3 == 1) {
                int64_t hi = next_random(&seed);
                int64_t lo = next_random(&seed);
                v = (hi * 65536 + lo) % 2000000001 - 1000000000;
            } else {
                v = 1000000000 - i * 200000 - next_random(&seed) % 100000;
            }
            all[c * n + i] = v;
        }
    }
    int64_t found = 0, checksum = 0;
    for (int64_t c = 0; c < arrays; c++) {
        for (int64_t r = 0; r < rounds; r++) {
            int64_t *answer = next_greater_elements(all + c * n, n);
            int64_t sum = 0;
            for (int64_t i = 0; i < n; i++) {
                sum += answer[i];
                if (answer[i] != -1) found++;
            }
            free(answer);
            checksum = (checksum * 31 + sum % 1000000007 + 1000000007) % 1000000007;
        }
    }
    printf("%lld arrays of %lld numbers, %lld times each: %lld with a greater one, checksum %lld\n",
           (long long)arrays, (long long)n, (long long)rounds, (long long)found, (long long)checksum);
    free(all);
    return 0;
}
