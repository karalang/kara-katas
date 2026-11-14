// LeetCode #1533: Find the Index of the Large Integer -- bench: the ★ arm
// (ternary search) over 100 readers of 2 to 100000 values, built once, each
// searched 20000 times. C mirror of index.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *sums;
    int32_t n;
    int64_t calls;
} ArrayReader;

static int32_t compare_sub(ArrayReader *reader, int32_t l, int32_t r, int32_t x, int32_t y) {
    reader->calls += 1;
    int64_t left = reader->sums[r + 1] - reader->sums[l];
    int64_t right = reader->sums[y + 1] - reader->sums[x];
    return left > right ? 1 : left < right ? -1 : 0;
}

static int32_t length(ArrayReader *reader) { return reader->n; }

static int64_t get_index(ArrayReader *reader) {
    int32_t lo = 0, hi = length(reader) - 1;
    while (lo < hi) {
        int32_t third = (hi - lo + 1) / 3;
        if (third == 0) {
            return compare_sub(reader, lo, lo, hi, hi) > 0 ? lo : hi;
        }
        int32_t second = lo + third;
        int32_t c = compare_sub(reader, lo, second - 1, second, second + third - 1);
        if (c == 1) {
            hi = second - 1;
        } else if (c == -1) {
            lo = second;
            hi = second + third - 1;
        } else {
            lo = second + third;
        }
    }
    return lo;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1533;
    ArrayReader readers[100];
    for (int k = 0; k < 100; k++) {
        int64_t a = next_random(&seed);
        int64_t n = (a * 32768 + next_random(&seed)) % 99999 + 2;
        int64_t base = next_random(&seed) % 99 + 1;
        int64_t large = base + next_random(&seed) % (100 - base) + 1;
        int64_t b = next_random(&seed);
        int64_t at = (b * 32768 + next_random(&seed)) % n;
        int64_t *sums = malloc((n + 1) * sizeof(int64_t));
        sums[0] = 0;
        for (int64_t i = 0; i < n; i++) {
            sums[i + 1] = sums[i] + (i == at ? large : base);
        }
        readers[k] = (ArrayReader){sums, (int32_t)n, 0};
    }
    int64_t check = 0;
    for (int p = 0; p < 20000; p++) {
        for (int k = 0; k < 100; k++) {
            check = mix(check, get_index(&readers[k]));
        }
    }
    int64_t calls = 0;
    for (int k = 0; k < 100; k++) {
        calls += readers[k].calls;
        free(readers[k].sums);
    }
    printf("20000 passes over 100 readers of up to 100000 values: checksum %lld, %lld calls\n", (long long)check,
           (long long)calls);
    return 0;
}
