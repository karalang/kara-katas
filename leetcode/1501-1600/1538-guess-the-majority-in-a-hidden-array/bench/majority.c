// LeetCode #1538: Guess the Majority in a Hidden Array -- bench: the ★ arm
// (every bit compared with bit 0, n queries) over 100 readers of 5 to 50000
// bits, built once, each asked 20 times. C mirror of majority.kara.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *nums;
    int32_t n;
    int64_t calls;
} ArrayReader;

static int32_t query(ArrayReader *reader, int32_t a, int32_t b, int32_t c, int32_t d) {
    reader->calls += 1;
    int64_t ones = reader->nums[a] + reader->nums[b] + reader->nums[c] + reader->nums[d];
    return (ones == 0 || ones == 4) ? 4 : ones == 2 ? 0 : 2;
}

static int32_t length(ArrayReader *reader) { return reader->n; }

static int64_t guess_majority(ArrayReader *reader) {
    int32_t n = length(reader);
    int32_t q0123 = query(reader, 0, 1, 2, 3);
    int32_t q1234 = query(reader, 1, 2, 3, 4);
    bool *same = malloc(n * sizeof(bool));
    same[0] = true;
    same[1] = query(reader, 0, 2, 3, 4) == q1234;
    same[2] = query(reader, 0, 1, 3, 4) == q1234;
    same[3] = query(reader, 0, 1, 2, 4) == q1234;
    same[4] = q1234 == q0123;
    for (int32_t i = 5; i < n; i++) {
        same[i] = query(reader, 1, 2, 3, i) == q0123;
    }
    int64_t with_zero = 0, other = -1;
    for (int32_t i = 0; i < n; i++) {
        if (same[i]) {
            with_zero += 1;
        } else {
            other = i;
        }
    }
    free(same);
    if (with_zero * 2 > n) return 0;
    if (with_zero * 2 < n) return other;
    return -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1538;
    ArrayReader readers[100];
    for (int k = 0; k < 100; k++) {
        int64_t a = next_random(&seed);
        int64_t n = (a * 32768 + next_random(&seed)) % 49996 + 5;
        int64_t chance = next_random(&seed) % 101;
        int64_t *nums = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            nums[i] = next_random(&seed) % 100 < chance ? 1 : 0;
        }
        readers[k] = (ArrayReader){nums, (int32_t)n, 0};
    }
    int64_t check = 0;
    for (int p = 0; p < 20; p++) {
        for (int k = 0; k < 100; k++) {
            check = mix(check, guess_majority(&readers[k]));
        }
    }
    int64_t calls = 0;
    for (int k = 0; k < 100; k++) {
        calls += readers[k].calls;
        free(readers[k].nums);
    }
    printf("20 passes over 100 readers of up to 50000 bits: checksum %lld, %lld calls\n", (long long)check,
           (long long)calls);
    return 0;
}
